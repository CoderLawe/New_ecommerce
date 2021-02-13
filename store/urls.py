from django.contrib import admin
from django.urls import path,include,re_path
from .import views
from .views import *

urlpatterns = [
    path('',views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('process_order/', views.process_order, name="process_order"),


    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),

    path('create/', views.product_create, name="create"),


    path('category/', views.all_categories, name="category"),


    path('update_product/<str:pk>/', views.update_product, name="update_product"),


    path('update_order/<str:pk>/', views.update_order, name="update_order"),

    path('customer_details/<str:pk>/', views.customer_view_details, name="customer_details"),


    #path('update_order/<str:key>/', views.update_order, name="update_order"),

    path('delete_order/<str:pk>/', views.delete_order, name="delete_order"),

    path('delete_product/<str:pk>/', views.delete_product, name="delete_product"),


    path('admin-customer/', views.view_customer.as_view(), name="customer"),

    path("admin-home/", AdminHomeView.as_view(), name="admin_home"),

    path("admin-logout/", admin_logout_view, name="admin_logout"),

    path("admin-products/", admin_products.as_view(), name="admin_products"),

    path("admin-orders/", admin_orders.as_view(), name="admin_orders"),

    path("admin-delivering/", views.out_for_delivery, name="delivering"),

    path("admin-delivered/", views.delivered, name="delivered"),





    path('update_item/', views.updateItem, name="update_item"),
    path('update_guest_item/', views.updateGuest_item, name="update_item"),

    path('carousel_edit/', views.carousel_detail, name="carousel"),

    path('search/', views.Search, name="search"),

    path('chart/', views.ClubChartView.as_view(), name="chart"),


    re_path(r'^(?P<slug>[\w-]+)/$', views.product_detail, name='detail'),

    #re_path(r'^(?P<slug>[\w-]+)/$', views.admin_ordering, name='ordering'),

    

    #re_path(r'^(?P<slug>[\w-]+)/$', views.updateOrder, name='update_order'),

    path("admin-order/<int:pk>/", admin_ordering.as_view(),
         name="admindetail"),

    path('export/', views.Export, name="export"),

        #Excel Stuff
    


]