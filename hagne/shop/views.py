from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Product


def index(request):
    products = Product.objects.all()[:1]
    context = {"products": products}
    return render(request, 'shop/index.html', context)


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    print('images', product)
    return render(request, 'shop/product.html', {'product': product})


def cart(request):
    cart = request.session.get('cart', {})
    print('cart', cart)

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        print('test', product_id, quantity)
        if product_id not in cart:
            cart[product_id] = 0
        cart[product_id] += quantity
        request.session['cart'] = cart

    return render(request, 'shop/cart.html', {'cart': cart})


def search(request):
    q = request.GET.get('q')

    order_by = request.GET.get('order_by')
    if order_by is None or len(order_by) == 0:
        order_by = 'name'

    page = request.GET.get('page')
    if page is None:
        page = 1

    products = Product.objects.filter(name__contains=q).order_by(order_by)
    paginator = Paginator(products, 24)
    page_data = paginator.get_page(page)

    context = {'q': q, 'order_by': order_by, 'page': page_data, 'num_pages': paginator.num_pages}
    return render(request, 'shop/search.html', context=context)


def account(request):
    if request.method == 'GET':
        return render(request, 'shop/account.html')
        
    return HttpResponse('post')