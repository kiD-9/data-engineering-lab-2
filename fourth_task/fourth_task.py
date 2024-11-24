import pickle
import json


def load_products():
    with open('../data/fourth_task_products.json', 'rb') as f:
        return pickle.load(f)


def load_updates():
    with open('../data/fourth_task_updates.json', encoding='utf-8') as f:
        return json.load(f)


def save_products(products):
    with open('fourth_task_result.pkl', 'wb') as f:
        return pickle.dump(products, f)


def map_names_to_products(products):
    mapping = {}
    for product in products:
        mapping[product['name']] = product
    return mapping


products = load_products()
products_map = map_names_to_products(products)
updates = load_updates()

for command in updates:
    name = command['name']
    method = command['method']
    param = command['param']
    product = products_map[name]
    if method == 'add':
        product['price'] += param
    elif method == 'sub':
        product['price'] -= param
    elif method == 'percent+':
        product['price'] *= (1 + param)
    elif method == 'percent-':
        product['price'] *= (1 - param)

save_products(products)