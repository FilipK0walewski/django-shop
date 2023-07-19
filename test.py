import requests
from bs4 import BeautifulSoup

def main():
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
            print(category_name, parent)
            input()
            parent_id = None
            if parent is not None:
                parent_id = db_category_map[parent]
            
            category, created = Category.objects.get_or_create(**{'name': category_name})
            print(db_category_map)
            db_category_map[category_name] = category


if __name__ == '__main__':
    main()
