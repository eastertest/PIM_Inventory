from django.urls import path, register_converter
from prod_inventory_app import views
import datetime


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value):
        return value


register_converter(DateConverter, 'date')


urlpatterns = [
    path('home/', views.home, name="home"),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_detail_chart/<int:product_id>/weeks<int:weeks>', views.product_detail_chart, name='product_detail_chart'),
    path('add_product/', views.add_product, name='add_product'),
    path('sell_item/<str:pk>/', views.sell_item, name='sell_item'),
    path('add_to_stock/<str:pk>/', views.add_to_stock, name='add_to_stock'),
    path('all_sales/', views.all_sales, name='all_sales'),
##    path('all_sales/<date:t_date>/<date:f_date>/', views.all_sales, name='all_sales'),
    path('receipt/', views.receipt, name="receipt"),
    path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    path('stock/', views.stock_search, name='stock'),
    path('export_products_csv/', views.export_products_csv, name='export_products_csv'),
    path('export_sales_csv/', views.export_sales_csv, name='export_sales_csv'),
    path('export_stock_csv/_csv/', views.export_stock_csv, name='export_stock_csv')
]
