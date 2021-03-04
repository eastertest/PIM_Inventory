from django.shortcuts import render, redirect
from django.http import HttpResponse
from prod_inventory_app.forms import ProductForm, ReceivedForm, SaleForm
from prod_inventory_app.filters import ProductFilter, ReceivedFilter, SaleFilter
import datetime
import csv
from django.core.mail import send_mail

from .models import Product, Received, Sale


def home(request):
    products = Product.objects.all().order_by('-id')
    product_filters = ProductFilter(request.GET, queryset=products)
    products = product_filters.qs

    return render(request, 'prod_inventory_app/index.html', {
        'products': products, 'product_filters': product_filters,
    })


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request,
                  'prod_inventory_app/product_detail.html',
                  {'product': product})


def product_detail_chart(request, product_id, weeks):
    end = datetime.date.today()
    start = end - datetime.timedelta(weeks=weeks)
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    quantity_list = []
    for date in date_generated:
        print(date)
        product = Product.objects.get(id=product_id)
        quantity = product.quantityovertime(date)
        quantity_list.append(quantity)
        print(quantity)

    return render(request, 'prod_inventory_app/chart.html', {
        'dates': date_generated,
        'quantity': quantity_list, })


def add_product(request):
    form = ProductForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.save()
            return redirect('home')

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
    sales = Sale.objects.all()
    total = sum([sale.quantity * sale.unit_price for sale in sales])
    change = sum([sale.get_change() for sale in sales])
    net = total - change
    sale_filters = SaleFilter(request.GET, queryset=sales)
    sale = sale_filters.qs
    return render(request, 'prod_inventory_app/all_sales.html',
                  {
                      'sales': sales,
                      'total': total,
                      'change': change,
                      'net': net,
                      'sale_filters': sale_filters,
                      'sale': sale,
                  })


def stock_search(request):
    product = Product.objects.all().order_by('-id')
    received = Received.objects.all().order_by('-id')
    product_filters = ProductFilter(request.GET, queryset=product)
    received_filters = ReceivedFilter(request.GET, queryset=received)
    products = product_filters.qs
    received = received_filters.qs
    return render(request, 'prod_inventory_app/stock_data.html', {
        'product': products, 'product_filters': product_filters,
        'received': received, 'received_filters': received_filters,
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
