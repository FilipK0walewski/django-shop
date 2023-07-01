import psycopg2
import requests

from bs4 import BeautifulSoup
from psycopg2.extras import execute_values


def main():
    # res = requests.get('https://dropshipping.hagne.pl/module/xmlfeeds/api?id=12')
    with open('12.xml', 'r') as f:
        data = f.read()

    soup = BeautifulSoup(data, 'xml')

    products = set()
    data, images = [], {}
    for p in soup.find('products').find_all('product'):
        product_id = p.find('id').text
        if product_id in products:
            continue
        products.add(product_id)

        manufacturer = p.find('manufacturer').text
        ean = p.find('ean13').text
        quantity = p.find('quantity').text
        description = p.find('description').text
        name = p.find('name').text
        category = p.find('category').text
        price = p.find('price').text.replace(',', '.')
        tax_rate = p.find('tax_rate').text
        product_category_tree = p.find('product_category_tree').text
        color = p.find('Kolor').text if p.find('Kolor') is not None else None

        product_images, found_images = [], p.find('images')
        if found_images is not None:
            for i in found_images.find_all('thickbox'):
                product_images.append(i.text)
            images[product_id] = product_images

        product = (manufacturer, product_id, ean, quantity, description, name, category, price, tax_rate, product_category_tree, color)
        data.append(product)

    print(len(data))
    conn = psycopg2.connect(database='hagne', user='filip', password='123', host='localhost')
    cur = conn.cursor()

    query = 'insert into shop_product(manufacturer, product_id, ean, quantity, description, name, category, price, tax_rate, product_category_tree, color) values %s'
    execute_values(cur, query, data)

    cur.execute('select id, product_id from shop_product')
    products_map = {product_id: i for i, product_id in cur}

    images_data = []
    for product_id, images_list in images.items():
        for url in images_list:
            images_data.append((products_map[product_id], url))
    
    execute_values(cur, 'insert into shop_image (product_id_id, url) values %s', images_data)
    conn.commit()


if __name__ == '__main__':
    main()
