from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from prod_inventory_app.forms import ProductForm, ReceivedForm, SaleForm, RemoveForm
from prod_inventory_app.filters import ProductFilter, ReceivedFilter, SaleFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import csv, io
from django.core.mail import send_mail
from django.contrib import messages
from .models import Product, Received, Sale


def home(request):
    products = Product.objects.all().order_by('-id')
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
    end = datetime.date.today()
    start = end - datetime.timedelta(weeks=weeks)
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]
    quantity_list = []
    date_list = []
    product = Product.objects.get(id=product_id)
    for date in date_generated:
        quantity = product.quantityovertime(date)
        quantity_list.append(quantity)
        date_list.append(str(date))

    return render(request, 'prod_inventory_app/chart.html', {
        'dates': date_list,
        'quantity': quantity_list,
        'product': product,
        'title': str(product) + " over " + str(weeks) + " weeks",
    })


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
        return render(request, 'prod_inventory_app/sucess.html', context)

    return render(request, 'prod_inventory_app/add_product.html', {'form': form})


def add_to_stock(request, pk):
    today = datetime.date.today()
    product1 = Product.objects.get(id=pk)
    received = Received(product=product1, date=today)
    form = ReceivedForm(instance=received)

    if request.method == 'POST':
        form = ReceivedForm(request.POST)
        if form.is_valid():
            received.date = form.cleaned_data['date']
            received.quantity = form.cleaned_data['quantity']
            received.vendor = form.cleaned_data['vendor']
            received.unit_price = form.cleaned_data['unit_price']
            received.save()
            send_mail('PIM INVENTORY Added Stock', 'HELLO, NEW INVENTORY has been added.',
                      'postmaster@sandbox065515e5489f4b25b5eecea694b9d197.mailgun.org', ['mercado.ismael@gmail.com'])
            return redirect('home')

    return render(request, 'prod_inventory_app/add_to_stock.html', {'form': form, 'product': product1.name})


def sell_item(request, pk):
    today = datetime.date.today()
    product1 = Product.objects.get(id=pk)
    sale = Sale(product=product1, date=today)
    form = SaleForm(instance=sale)

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale.date = form.cleaned_data['date']
            sale.customer = form.cleaned_data['customer']
            sale.quantity = form.cleaned_data['quantity']
            sale.unit_price = form.cleaned_data['unit_price']
            sale.payment_received = form.cleaned_data['payment_received']
            sale.save()
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
    total = sum([sale.quantity * sale.unit_price for sale in sales])
    change = sum([sale.get_change() for sale in sales])
    net = total - change
    sale_filters = SaleFilter(request.GET, queryset=sales)
    sale = sale_filters.qs
    paginator = Paginator(sale, 20)
    page = request.GET.get('page')
    sale = paginator.get_page(page)

    prompt = {'sales': sales,
              'total': total,
              'change': change,
              'net': net,
              'sale_filters': sale_filters,
              'sale': sale,
              'page': page,
              }
    if request.method == "GET":
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
                product_id=column[1],
                customer=column[2],
                quantity=column[3],
                unit_price=column[4],
                payment_received=column[5]
            )
        context = {}
        return render(request, 'prod_inventory_app/sucess.html', context)


def stock_search(request):
    product = Product.objects.all().order_by('-id')
    received = Received.objects.all().order_by('-id')
    product_filters = ProductFilter(request.GET, queryset=product)
    received_filters = ReceivedFilter(request.GET, queryset=received)
    products = product_filters.qs
    received = received_filters.qs
    paginator = Paginator(received, 20)
    page = request.GET.get('page')
    received = paginator.get_page(page)
    return render(request, 'prod_inventory_app/stock_data.html', {
        'product': products, 'product_filters': product_filters,
        'received': received, 'received_filters': received_filters,
        'page': page,
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
    writer.writerow(['order date', 'product', 'quantity received', 'vendor', 'cost'])

    stock = Received.objects.all()
    for received in stock:
        writer.writerow([received.date, received.product, received.quantity, received.vendor, received.unit_price])
    return response


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
                product_id=column[1],
                quantity=column[2],
                vendor=column[3],
                unit_price=column[4],
            )
        context = {}
        return render(request, 'prod_inventory_app/sucess.html', context)


def remove_item(request, pk):
    today = datetime.date.today()
    product1 = Product.objects.get(id=pk)
    sale = Sale(product=product1, date=today)
    form = RemoveForm(instance=sale)

    if request.method == 'POST':
        form = RemoveForm(request.POST)
        if form.is_valid():
            sale.date = form.cleaned_data['date']
            sale.quantity = form.cleaned_data['quantity']
            sale.save()
            return redirect('home')

    return render(request, 'prod_inventory_app/remove.html', {'remove_form': form, 'product': product1.name})
