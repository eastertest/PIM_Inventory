from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpRequest
from prod_inventory_app.forms import SignUpForm, ProductForm, ReceivedForm, SaleForm, RemovedForm
from prod_inventory_app.filters import ProductFilter, ReceivedFilter, SaleFilter
from prod_inventory_app.tokens import account_activation_token
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import csv, io
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Product, Received, Sale, Removed, Vendor
import os
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all().order_by('id')
    product_filters = ProductFilter(request.GET, queryset=products)
    products = product_filters.qs
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'prod_inventory_app/index.html', {
        'products': products, 'product_filters': product_filters, 'page': page})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request,
                  'prod_inventory_app/product_detail.html',
                  {'product': product})


def product_detail_chart(request, product_id, weeks):
    now = datetime.datetime.now()
    end = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=23, minute=59)
    start = end - datetime.timedelta(weeks=weeks)
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]
    quantity_list = []
    date_list = []
    predicted_list = []
    product = Product.objects.get(id=product_id)
    for date in date_generated:
        quantity = product.quantityovertime(date)
        quantity_list.append(quantity)
        date_list.append(str(date))

    date_zero = product.inventory_zero()
    if date_zero != -1:
        date_list.append(str(date_zero))
        for i in quantity_list[:-1]:
            predicted_list.append('null')
        predicted_list.append(quantity_list[-1])
        predicted_list.append(0)
        quantity_list.append('null')
        print(predicted_list)

    return render(request, 'prod_inventory_app/chart.html', {
        'dates': date_list,
        'quantity': quantity_list,
        'predicted': predicted_list,
        'product': product,
        'title': str(product) + " over " + str(weeks) + " weeks",
    })

@login_required
def add_product(request):
    form = ProductForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.save()
            return redirect('home')

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Product.objects.update_or_create(
                name=column[0],
                description=column[1],
            )
        context = {}
        return render(request, 'prod_inventory_app/success.html', context)

    return render(request, 'prod_inventory_app/add_product.html', {'form': form})


@login_required
def add_to_stock(request, pk):
    today = datetime.datetime.now()
    product1 = Product.objects.get(id=pk)
    received = Received(product=product1, date=today)
    form = ReceivedForm(instance=received)

    if request.method == 'POST':
        form = ReceivedForm(request.POST)
        if form.is_valid():
            received.date = datetime.datetime.now()
            received.quantity = form.cleaned_data['quantity']
            received.vendor1 = form.cleaned_data['vendor1']
            received.unit_price = form.cleaned_data['unit_price']
            received.save()
            send_mail('PIM INVENTORY Added Stock', 'HELLO, ' +  product1.name + ' has been added.',
                      os.getenv("EMAIL_HOST_USER"), [request.user.email])
            return redirect('home')

    return render(request, 'prod_inventory_app/add_to_stock.html', {'form': form, 'product': product1.name})



@login_required
def sell_item(request, pk):
    today = datetime.datetime.now()
    product1 = Product.objects.get(id=pk)
    sale = Sale(product=product1, date=today)
    form = SaleForm(instance=sale)

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale.date = datetime.datetime.now()
            sale.customer = form.cleaned_data['customer']
            sale.quantity = form.cleaned_data['quantity']
            sale.unit_price = form.cleaned_data['unit_price']
            sale.payment_received = form.cleaned_data['payment_received']

            if sale.get_change() > 0:
                form.clean()
                messages.warning(request, 'Not enough Funds to complete the transaction.')
            else:
                sale.save()
                if product1.quantity() < 10:
                    messages.success(request, 'Your stock of ' + product1.name + ' is currently low, there is only ' + str(product1.quantity()) + ' left. Please refill.')
                    send_mail('PIM INVENTORY Low Stock Alert', 'Your stock of ' + product1.name + ' is currently low, there is only ' + str(product1.quantity()) + ' left. Please refill.', os.getenv("EMAIL_HOST_USER"), [request.user.email])
                return redirect('receipt')

    return render(request, 'prod_inventory_app/issue_item.html', {'sales_form': form, 'product': product1.name})


def receipt(request):
    sales = Sale.objects.all().order_by('-id')
    return render(request, 'prod_inventory_app/receipt.html', {'sales': sales, })


def receipt_detail(request, receipt_id):
    receipt = Sale.objects.get(id=receipt_id)
    return render(request, 'prod_inventory_app/receipt_detail.html', {'receipt': receipt})


def all_sales(request):
    template = 'prod_inventory_app/all_sales.html'
    sales = Sale.objects.all().order_by('-date')
    sale_filters = SaleFilter(request.GET, queryset=sales)
    sale = sale_filters.qs
    paginator = Paginator(sale, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    prompt = {'sale_filters': sale_filters,
              'sale': sale,
              'page_obj': page_obj,
              }
    if request.method == "GET":
        if request.GET.get('download', None) == 'csv':
            sale = sale_filters.qs
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="sales.csv"'

            writer = csv.writer(response)
            writer.writerow(['date sold (yyyy-mm-dd HH:MM)', 'item bought (string)', 'customer name (string)', 'quantity (integer)', 'unit price (float)', 'payment received (float)'])
            for s in sale:
                writer.writerow([s.date, s.product, s.customer, s.quantity, s.unit_price, s.payment_received])
            return response
        else:
            return render(request, template, prompt)
    if request.method == 'POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Sale.objects.update_or_create(
                date=column[0],
                product_id=Product.objects.update_or_create(name=column[1].lower())[0].id,
                customer=column[2],
                quantity=column[3],
                unit_price=column[4],
                payment_received=column[5]
            )
        context = {}
        return render(request, 'prod_inventory_app/success.html', context)


def stock_search(request):
    template = 'prod_inventory_app/stock_data.html'
    received = Received.objects.all().order_by('-id')
    received_filters = ReceivedFilter(request.GET, queryset=received)
    received = received_filters.qs
    paginator = Paginator(received, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    prompt = {'received_filters': received_filters,
              'page_obj': page_obj,
        }
    if request.method == "GET":
        if request.GET.get('download', None) == 'csv':
            received = received_filters.qs
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="stock.csv"'

            writer = csv.writer(response)
            writer.writerow(['date (yyyy-mm-dd HH:MM)', 'product (string)', 'quantity received (integer)', 'vendor1 (string)', 'cost (float)'])
            for r in received:
                writer.writerow([r.date, r.product, r.quantity, r.vendor1, r.unit_price])
            return response
        else:
            return render(request, template, prompt)
    if request.method == 'POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Received.objects.update_or_create(
                date=column[0],
                product_id=Product.objects.update_or_create(name=column[1].lower())[0].id,
                quantity=column[2],
                vendor1=Vendor.objects.update_or_create(vendor=column[3].lower())[0],
                unit_price=column[4],
            )
        context = {}
        return render(request, 'prod_inventory_app/success.html', context)

    return render(request, 'prod_inventory_app/stock_data.html', {
        'received_filters': received_filters,
        'page_obj': page_obj,
    })


def export_products_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'description', 'quantity'])

    products = Product.objects.all()
    for product in products:
        writer.writerow([product.name, product.description, product.quantity()])
    return response


def export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales.csv"'

    writer = csv.writer(response)
    writer.writerow(['date sold', 'customer name', 'item bought', 'quantity', 'unit price', 'payment received'])

    sales = Sale.objects.all()
    for sale in sales:
        writer.writerow([sale.date, sale.customer, sale.product, sale.quantity, sale.unit_price, sale.payment_received])
    return response


def export_stock_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock.csv"'

    writer = csv.writer(response)
    writer.writerow(['order date', 'product', 'quantity received', 'vendor1', 'cost'])

    stock = Received.objects.all()
    for received in stock:
        writer.writerow([received.date, received.product, received.quantity, received.vendor1, received.unit_price])
    return response


@login_required
def add_to_stock_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            _, created = Received.objects.update_or_create(
                date=column[0],
                product_id=Product.objects.update_or_create(name=column[1].lower())[0].id,
                quantity=column[2],
                vendor1=Vendor.objects.update_or_create(vendor=column[3].lower())[0],
                unit_price=column[4],
            )
        context = {}
        return render(request, 'prod_inventory_app/success.html', context)


@login_required
def remove_item(request, pk):
    today = datetime.datetime.now()
    product1 = Product.objects.get(id=pk)
    remove = Removed(product=product1, date=today)
    form = RemovedForm(instance=remove)

    if request.method == 'POST':
        form = RemovedForm(request.POST)
        if form.is_valid():
            remove.date = datetime.datetime.now()
            remove.quantity = form.cleaned_data['quantity']
            remove.reason1 = form.cleaned_data['reason1']
            remove.save()
            if product1.quantity() < 10:
                messages.success(request, 'Your stock of ' + product1.name + ' is currently low, there is only ' + str(product1.quantity()) + ' left. Please refill.')
                send_mail('PIM INVENTORY Low Stock Alert', 'Your stock of ' + product1.name + ' is currently low, there is only ' + str(product1.quantity()) + ' left. Please refill.', os.getenv("EMAIL_HOST_USER"), [request.user.email])
            return redirect('home')

    return render(request, 'prod_inventory_app/remove.html', {'remove_form': form, 'product': product1.name})


def reports(request):
    prods = Product.objects.all()
    product_filters = ProductFilter(request.GET, queryset=prods)
    products = product_filters.qs
    gross = Sale.gross_profit()
    trend = Sale.trends()
    rate_of_sale = Sale.rate_of_sales_growth()
    ytd = Sale.year_to_date_sales()
    products = products.order_by('id')
    context = {
        'gross':gross,
        'trend':trend,
        'rate_of_sale':rate_of_sale,
        'ytd':ytd,
        'products':products,
    }
    return render(request, 'prod_inventory_app/reports.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your PIM Inventory Account'
            message = render_to_string('prod_inventory_app/account_activation_email.html', {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'prod_inventory_app/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'prod_inventory_app/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'prod_inventory_app/account_activation_invalid.html')
