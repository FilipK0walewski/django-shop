import psycopg2
    
conn = psycopg2.connect(database='hagne', user='filip', password='123', host='localhost')
cur = conn.cursor()


def get_categories(parent_id):
    cur.execute('select id, name from shop_category where parent_id = %s', (parent_id,))
    categories = cur.fetchall()

    if len(categories) == 0:
        return None

    leafs = []
    for category_id, category_name in categories:
        tmp = get_categories(category_id)
        leafs.append({'id': category_id, 'name': category_name, 'leafs': tmp})

    return leafs

cur.execute('select id, name from shop_category where parent_id is null')
parents = [i for i in cur]

category_tree = {}
for category_id, name in parents:
    tree = get_categories(category_id)
    category_tree[category_id] = {'name': name, 'leafs': tree}

print(category_tree)