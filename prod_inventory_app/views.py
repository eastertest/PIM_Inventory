from django.shortcuts import render, redirect
from prod_inventory_app.forms import AddForm, SaleForm
from prod_inventory_app.filters import ProductFilter

from django.shortcuts import render
from prod_inventory_app.models import Product
from prod_inventory_app.models import Restock
from prod_inventory_app.models import Sale


def home(request):
    products = Product.objects.all().order_by('-id')
    product_filters = ProductFilter(request.GET, queryset = products)
    products = product_filters.qs

    return render(request, 'products/index.html', {
        'products': products, 'product_filters': product_filters,
    })
	

def product_detail(request, product_id):
    product = Product.objects.get(id = product_id)
    return render(request, 
                 'products/product_detail.html',
                 {'product': product})


def add_to_stock(request, pk):
    issued_item = Product.objects.get(id = pk)
    form = AddForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            new_add = form.save(commit=False)
            new_add.save()
            added_quantity = int(request.POST['quantity_received'])
            issued_item.total_quantity += added_quantity
            issued_item.save()
            print(added_quantity)
            print (issued_item.total_quantity)
            return redirect('home')

    return render (request, 'products/add_to_stock.html', {'form': form})


def issue_item(request, pk):
    issued_item = Product.objects.get(id = pk)
    sales_form = SaleForm(request.POST)  

    if request.method == 'POST':     
        if sales_form.is_valid():
            new_sale = sales_form.save(commit=False)
            new_sale.item = issued_item
            new_sale.unit_price = issued_item.unit_price   
            new_sale.save()
            quantity_issued = int(request.POST['quantity_issued'])
            issued_item.total_quantity -= quantity_issued
            issued_item.save()
            return redirect('receipt') 
    return render (request, 'products/issue_item.html', {'sales_form': sales_form,})


def receipt(request): 
    sales = Sale.objects.all().order_by('-id')
    return render(request, 'products/receipt.html', {'sales': sales,})


def receipt_detail(request, receipt_id):
    receipt = Sale.objects.get(id = receipt_id)
    return render(request, 'products/receipt_detail.html', {'receipt': receipt})


def all_sales(request):
    sales = Sale.objects.all()
    total  = sum([items.payment_received for items in sales])
    change = sum([items.get_change() for items in sales])
    net = total - change
    return render(request, 'products/all_sales.html',
     {
     'sales': sales, 
     'total': total, 
	 'change': change,
     'net': net,
      })

