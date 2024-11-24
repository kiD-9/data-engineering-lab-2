import os.path
import json
import msgpack


def load_json():
    with open('../data/third_task.json', encoding='utf-8') as f:
        return json.load(f)


def get_items_stats(data):
    items = {}
    for item in data:
        name = item['name']
        price = item['price']
        if name not in items:
            items[name] = {
                'name': name,
                'sum': price,
                'max': price,
                'min': price,
                'count': 1
            }
        else:
            items[name]['count'] += 1
            items[name]['sum'] += price
            if price > items[name]['max']:
                items[name]['max'] = price
            if price < items[name]['min']:
                items[name]['min'] = price

    for k, v in items.items():
        v['avg'] = v['sum'] / v['count']
        v.pop('sum')
        v.pop('count')
    return items



data = load_json()
stats = get_items_stats(data)
result = list(stats.values())

with open('third_task_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False)

with open("third_task_result.msgpack", "wb") as f:
    packed = msgpack.packb(result)
    f.write(packed)

# файл msgpack меньше на ~ 3000 байт
json_size = os.path.getsize('third_task_result.json')
msgpack_size = os.path.getsize('third_task_result.msgpack')
size_comparison = (f'json size = {json_size} bytes\n'
                   f'msgpack size = {msgpack_size} bytes\n'
                   f'diff = {json_size - msgpack_size} bytes\n')

with open('size_comparison.txt', 'w') as f:
    f.write(size_comparison)
print(size_comparison)