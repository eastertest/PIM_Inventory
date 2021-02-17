from django.shortcuts import render, redirect
from prod_inventory_app.forms import ProductForm, RestockForm, SaleForm
from prod_inventory_app.filters import ProductFilter
import datetime

from .models import Product, Restock, Sale


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
    restock = Restock(product=product1, order_date=today)
    form = RestockForm(instance=restock)

    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            restock.order_date = form.cleaned_data['order_date']
            restock.quantity_ordered = form.cleaned_data['quantity_ordered']
            restock.quantity_received = form.cleaned_data['quantity_received']
            restock.vendor = form.cleaned_data['vendor']
            restock.vendor_cost = form.cleaned_data['vendor_cost']
            product1.total_quantity += restock.quantity_received
            restock.save()
            product1.save()
            return redirect('home')

    return render(request, 'prod_inventory_app/add_to_stock.html', {'form': form})


def sell_item(request, pk):
    today = datetime.date.today()
    product1 = Product.objects.get(id=pk)
    sale = Sale(product=product1, sale_date=today)
    form = SaleForm(instance=sale)

    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale.sale_date = form.cleaned_data['sale_date']
            sale.customer = form.cleaned_data['customer']
            sale.quantity_issued = form.cleaned_data['quantity_issued']
            sale.unit_price = form.cleaned_data['unit_price']
            sale.payment_received = form.cleaned_data['payment_received']
            product1.total_quantity -= sale.quantity_issued
            sale.save()
            product1.save()
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
    total = sum([product.quantity_issued * product.unit_price for product in sales])
    change = sum([items.get_change() for items in sales])
    net = total - change
    return render(request, 'prod_inventory_app/all_sales.html',
                  {
                      'sales': sales,
                      'total': total,
                      'change': change,
                      'net': net,
                  })
