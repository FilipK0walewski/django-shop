from django.urls import path, re_path

from . import views

# app_name = 'shop'
urlpatterns = [
    path('', views.index, name='home'),
    path('account/', views.account, name='login'),

    path('search/', views.search, name='search'),
    path('search/<int:category_id>', views.category, name='category'),

    path('cart/', views.cart, name='cart'),
    path('cart/items/', views.get_cart_items),
    path('cart/<str:product_id>/increment/', views.increment_cart_item),
    path('cart/<str:product_id>/decrement/', views.decrement_cart_item),
    path('cart/<str:product_id>/delete/', views.delete_cart_item),
    path('cart/submit/', views.submit_cart, name='submit-cart'),

    path('transaction/<str:transaction_id>/order/', views.get_transaction_order, name='transaction-order'),

    path('product/<int:product_id>/', views.detail, name='detail'),
]
