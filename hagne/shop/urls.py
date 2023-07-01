from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('account/', views.account, name='login'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:product_id>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
]
