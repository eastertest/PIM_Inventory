
from django.urls import path
from prod_inventory_app import views


urlpatterns = [
path('home/', views.home, name = "home"),
path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
path('add_product/', views.add_product, name='add_product'),
path('sell_item/<str:pk>/', views.sell_item, name='sell_item'),
path('add_to_stock/<str:pk>/', views.add_to_stock, name='add_to_stock'),
path('all_sales/', views.all_sales, name = 'all_sales'),
path('receipt/', views.receipt, name = "receipt"),
path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
path('search/', views.search, name='search'),
path('product_detail_chart/<int:product_id>/weeks<int:weeks>', views.product_detail_chart, name='product_detail_chart')
]
