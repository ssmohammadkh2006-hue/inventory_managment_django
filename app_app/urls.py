from django.urls import path
from . import views

urlpatterns = [
    # Home / Dashboard
 
    path('', views.user_login, name='login'),
 
    path('index/', views.index, name='index'),

    # pdf تصدير ----------------------------------------------------
    path('export-products-pdf/', views.export_products_pdf, name='export_products_pdf'),
    path('export_distributors_pdf', views.export_distributors_pdf, name='export_distributors_pdf'),
    path('export_sales_pdf', views.export_sales_pdf, name='export_sales_pdf'),
    
    
    
    path('about/', views.About_System, name='About_System'),
    # search ---------------------------------------------------------
    

    # Product URLs ---------------------------------------------------------
    path('add_product/', views.add_product, name='add_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),

    # Distributors URLs ---------------------------------------------------------
    path('add_distributor/', views.add_distributors, name='add_distributors'),
    path('distributors_list/', views.distributors_list, name='distributors_list'),
    path('update_distributor/<int:id>/', views.update_distributors, name='update_distributors'),

    # Sales URLs ---------------------------------------------------------
    path('sales_product/', views.sales_prodect, name='sales_prodect'),
    path('sales_list/', views.sales_list, name='sales_list'),
    path('update_sales/<int:id>/', views.update_sales, name='update_sales'),

    # Delete Confirmation ---------------------------------------------------------
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('delete_distributor/<int:id>/', views.delete_distributor, name='delete_distributor'),
    path('delete_sale/<int:id>/', views.delete_sale, name='delete_sale'),
]