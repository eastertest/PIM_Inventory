
from django.urls import path
from prod_inventory_app import views


urlpatterns = [
path('home/', views.home, name = "home"),
path('home/<int:product_id>/', views.product_detail, name='product_detail'),
path('issue_item/<str:pk>/', views.issue_item, name='issue_item'),
path('add_to_stock/<str:pk>/', views.add_to_stock, name='add_to_stock'),
path('all_sales/', views.all_sales, name = 'all_sales'),
path('receipt/', views.receipt, name = "receipt"),
path('receipt/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
]