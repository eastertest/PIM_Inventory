from django.shortcuts import render, redirect
from prod_inventory_app.forms import ProductForm, ReceivedForm, SaleForm
from prod_inventory_app.filters import ProductFilter, ReceivedFilter, SaleFilter
import datetime
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
            send_mail('PIM INVENTORY Added Stock', 'HELLO, NEW INVENTORY has been added.', 'postmaster@sandbox065515e5489f4b25b5eecea694b9d197.mailgun.org', ['mercado.ismael@gmail.com'])
            return redirect('home')
    
    return render(request, 'prod_inventory_app/add_to_stock.html', {'form': form})


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

    return render(request, 'prod_inventory_app/issue_item.html', {'sales_form': form, })


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
    return render(request, 'prod_inventory_app/all_sales.html',
                  {
                      'sales': sales,
                      'total': total,
                      'change': change,
                      'net': net,
                  })


def search(request):
    product = Product.objects.all().order_by('-id')
    received = Received.objects.all().order_by('-id')
    sale = Sale.objects.all().order_by('-id')

    product_filters = ProductFilter(request.GET, queryset=product)
    received_filters = ReceivedFilter(request.GET, queryset=received)
    sale_filters = SaleFilter(request.GET, queryset=sale)

    products = product_filters.qs
    received = received_filters.qs
    sale = sale_filters.qs

    return render(request, 'prod_inventory_app/search_data.html', {
        'product': products, 'product_filters': product_filters,
        'received': received, 'received_filters': received_filters,
        'sale': sale, 'sale_filters': sale_filters,
    })
