import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
django.setup()

import json
import re

from server.restaurant.models import Restaurant, MenuItem, MenuSection

menus = {}

for fname in os.listdir('_dummy'):
    if not fname.startswith('MENU__'):
        continue
    restaurant_name = re.match('MENU__(.*)-Delivery', fname)[1].replace('-', ' ')
    with open('./_dummy/'+fname, 'r') as f:
        sections = json.loads(f.read())
    restaurant, new = Restaurant.objects.get_or_create(name=restaurant_name)
    if new:
        print('new restaurant', restaurant)
    menus[restaurant_name] = sections

menu_keys = list(menus.keys())

for restaurant in Restaurant.objects.all():
    if restaurant.menusection_set.all():
        print('skipping', restaurant)
        continue
    use_name = restaurant.name
    if not menus.get(use_name):
        use_name = menu_keys[restaurant.id % len(menu_keys)]
    for section in menus[use_name]:
        name = section['sectionTitle']
        items = zip(section['itemNames'], section['itemPrices'])
        menusection = MenuSection.objects.create(name=name,restaurant=restaurant)
        for name, price in items:
            price = float(price.replace('$',''))
            MenuItem.objects.create(name=name, price=price, menusection=menusection)