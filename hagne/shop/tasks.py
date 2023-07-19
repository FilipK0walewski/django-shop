import requests

from bs4 import BeautifulSoup
from celery import shared_task
from django.core.files import File
from django.db import transaction
from tempfile import NamedTemporaryFile

from hagne.celery import app
from shop.models import Category, Image, Product


@shared_task
def download_images():
    print('downloading images start')
    to_download = Image.objects.filter(downloaded__isnull=True)
    for image in to_download:
        r = requests.get(image.url)
        if r.status_code != 200:
            continue

        temp_image = NamedTemporaryFile(delete=True)
        temp_image.write(r.content)
        temp_image.flush()

        image_name = str(image.product_id) + '/' + image.url.split('/')[-1]
        image.downloaded.save(image_name, File(temp_image))
        image.save()
    print('end')


@shared_task
def update_stock():
    print('update stock start')
    r = requests.get('https://dropshipping.hagne.pl/module/xmlfeeds/api?id=13')
    print(f'response status code: {r.status_code}')
    if r.status_code != 200:
        return

    data = {}
    soup = BeautifulSoup(r.text, 'xml')
    for product in soup.find('stock').find_all('product'):
        product_id = product.find('id').text
        if product_id in data:
            continue
        quantity = product.find('quantity').text
        data[product_id] = quantity

    print(f'number of products: {len(data)}')
    products = Product.objects.all()
    with transaction.atomic():
        for product in products:
            if product.product_id not in data:
                continue
            product.quantity = data[product.product_id]
    Product.objects.bulk_update(products, ['quantity'])
    print('end')
    

@shared_task
def update_products():
    print('update products start')
    r = requests.get('https://dropshipping.hagne.pl/module/xmlfeeds/api?id=12')
    print(f'response status code: {r.status_code}')
    if r.status_code != 200:
        return

    soup = BeautifulSoup(r.text, 'xml')
    all_categories, products, images = {}, {}, {}
    for product in soup.find('products').find_all('product'):
        product_id = product.find('id').text
        if product_id in products:
            continue

        manufacturer = product.find('manufacturer').text
        ean = product.find('ean13').text
        quantity = product.find('quantity').text
        description = product.find('description').text
        name = product.find('name').text
        category = product.find('category').text
        price = product.find('price').text.replace(',', '.')
        tax_rate = product.find('tax_rate').text
        color = product.find('Kolor').text if product.find('Kolor') is not None else None

        categories = [i.strip() for i in product.find('product_category_tree').text.split('>')]
        for i in range(len(categories)):
            parent, category = None, categories[i]
            if i != 0:
                parent = categories[i - 1]
            if i not in all_categories:
                all_categories[i] = set()
            all_categories[i].add((category, parent))

        product_images, found_images = [], product.find('images')
        if found_images is not None:
            for i in found_images.find_all('thickbox'):
                product_images.append(i.text.strip())
            images[product_id] = product_images

        product = {
            'manufacturer': manufacturer, 
            'product_id': product_id, 
            'ean': ean, 
            'quantity': quantity, 
            'description': description, 
            'name': name, 
            'price': price, 
            'tax_rate': tax_rate, 
            'color': color, 
            'category': categories[-1]
        }
        products[product_id] = product

    print('updating categories')
    db_category_map = {}
    for i in all_categories.keys():
        for category_name, parent in all_categories[i]:
            parent_id = None
            if parent is not None:
                parent_id = db_category_map[parent]
            
            category, _ = Category.objects.get_or_create(name=category_name, parent=parent_id)
            db_category_map[category_name] = category

    print('updating products')
    db_product_map = {}
    for product_id, product_data in products.items():
        tmp = product_data['category']
        product_data['category'] = db_category_map[tmp]
        product, created = Product.objects.update_or_create(defaults=product_data, product_id=product_id)
        db_product_map[product_id] = product

    print('updating images')
    for product_id, product_images in images.items():
        for image in product_images:
            Image.objects.get_or_create(**{'url': image, 'product': db_product_map[product_id]})

    print('end')
