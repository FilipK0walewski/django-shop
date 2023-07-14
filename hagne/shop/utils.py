
def get_category_path(category_tree, category_id):
    queue = []
    for i in category_tree:
        queue.append([i])

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node['id'] == category_id:
            return path

        if node['children'] is None:
            continue

        for i in node['children']:
            queue.append(path + [i])

    return None


def get_subcategories(category_tree, category_id):
    subcategories = []

    def tmp(categories, is_children):
        if categories is None:
            return
        
        a = is_children
        for i in categories:
            print(category_id, i['id'])
            if is_children is False and i['id'] == category_id:
                a = True

            if a is True:
                subcategories.append(i['id'])

            print(i['id'], a)
            tmp(i['children'], a)

    a = False
    for i in category_tree:
        if i['id'] == category_id:
            a = True
        
        print(i['id'], a)
        tmp(i['children'], a)

    return subcategories
