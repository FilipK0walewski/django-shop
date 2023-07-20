from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render 
from django.urls import reverse

from .models import Product, Image, Category, ProductComment
from .utils import get_category_path, get_subcategories


def index(request):
    return render(request, 'shop/index.html', {'categories': Category.objects.get_category_tree()})


def search(request):
    q = request.GET.get('q', None)
    order_by = request.GET.get('order_by', 'price')
    page = request.GET.get('page', 1)

    if q is not None:
        products = Product.objects.filter(name__contains=q).order_by(order_by)
    else:
        products = Product.objects.all().order_by(order_by)

    paginator = Paginator(products, 24)
    page_data = paginator.get_page(page)

    categories = Category.objects.get_category_tree()

    context = {'page': page_data, 'num_pages': paginator.num_pages, 'categories': categories}
    return render(request, 'shop/search.html', context=context)


def category(request, category_id):
    q = request.GET.get('q', None)
    order_by = request.GET.get('order_by', 'price')
    page = request.GET.get('page', 1)

    categories = Category.objects.get_category_tree()
    category_path = get_category_path(categories, category_id)
    subcategories = Category.objects.get_subcategories(category_id)

    if q is not None:
        products = Product.objects.filter(category_id__in=subcategories).filter(name__contains=q).order_by(order_by)
    else:
        products = Product.objects.filter(category_id__in=subcategories).order_by(order_by)

    paginator = Paginator(products, 24)
    page_data = paginator.get_page(page)

    context = {
        'page': page_data,
        'num_pages': paginator.num_pages,
        'categories': categories,
        'category_path': category_path,
    }
    return render(request, 'shop/search.html', context=context)


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.get_category_tree()
    category_path = get_category_path(categories, product.category_id)
    comments = ProductComment.objects.filter(product_id=product_id)
    return render(request, 'shop/product.html', {'product': product, 'categories': categories, 'category_path': category_path, 'comments': comments})


def cart(request):
    cart = request.session.get('cart', {'items': {}, 'step': 0})

    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        if product_id not in cart['items']:
            cart['items'][product_id] = 0
        cart['items'][product_id] += quantity
        request.session['cart'] = cart
        return HttpResponseRedirect(reverse('cart'))
    
    categories = Category.objects.get_category_tree()
    return render(request, 'shop/cart.html', {'cart': cart, 'categories': categories})


def submit_cart(request):
    return HttpResponseRedirect(reverse('transaction-order', args=('123',)))


def get_transaction_order(request, transaction_id):
    return render(request, 'shop/transaction.html')


def get_cart_items(request):
    cart = request.session.get('cart', None)

    nice_cart = []
    for product_id, quantity in cart['items'].items():
        product = Product.objects.get(pk=product_id)
        cart_product = {
            'id': product_id,
            'name': f'{product.name} {product.manufacturer} {product.product_id}',
            'image': product.image_set.first().url,
            'price': product.price,
            'quantity': quantity,
            'stock': product.quantity,
        }
        nice_cart.append(cart_product)

    return JsonResponse({'cart': nice_cart})


def delete_cart_item(request, product_id):
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])

    cart = request.session.get('cart', None)
    if cart is None or product_id not in cart['items']:
        raise Http404('Not found.')

    del cart['items'][product_id]
    request.session['cart'] = cart
    return JsonResponse({'cart': cart})


def increment_cart_item(request, product_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', None)
    if cart is None or product_id not in cart['items']:
        raise Http404('Not found.')

    if cart['items'][product_id] == product.quantity:
        return HttpResponseBadRequest('Bad request.')

    value = min(product.quantity, cart['items'][product_id] + 1)
    cart['items'][product_id] = value
    request.session['cart'] = cart
    return HttpResponse('', status=204)


def decrement_cart_item(request, product_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', None)
    if cart is None or product_id not in cart['items']:
        raise Http404('Not found.')

    if cart['items'][product_id] == 1:
        return HttpResponseBadRequest('Bad request.')

    value = max(1, cart['items'][product_id] - 1)
    cart['items'][product_id] = value
    request.session['cart'] = cart
    return HttpResponse('', status=204)


def account(request):
    if request.user.is_authenticated is False:
        return redirect('login')

    return render(request, 'shop/account.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'shop/login.html')

    if request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Zalogowano jako {user.get_username()}.')
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.add_message(request, messages.ERROR, 'Niepoprawne dane logowania.')
        return HttpResponseRedirect(reverse('login'))


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, f'Wylogowano.')
    return HttpResponseRedirect(reverse('home'))


def registration(request):
    if request.method == 'GET':
        return render(request, 'shop/registration.html')

    if request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    username = request.POST.get('username', None)
    email = request.POST.get('email', None)
    password0 = request.POST.get('password0', None)
    password1 = request.POST.get('password1', None)

    if username is None:
        messages.add_message(request, messages.ERROR, 'Niepoprawna nazwa uzytkownika.')
        return HttpResponseRedirect(reverse('registration'))

    if email is None:
        messages.add_message(request, messages.ERROR, 'Niepoprawny email.')
        return HttpResponseRedirect(reverse('registration'))

    if password0 != password1:
        messages.add_message(request, messages.ERROR, 'Hasla nie sa takie same.')
        return HttpResponseRedirect(reverse('registration'))

    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, 'Uzytkownik o tej nazwie juz istnieje.')
        return HttpResponseRedirect(reverse('registration'))

    User.objects.create_user(username, email, password0)
    messages.add_message(request, messages.SUCCESS, 'Konto utworzone. Mozesz sie teraz zalogowac')
    return HttpResponseRedirect(reverse('login'))
