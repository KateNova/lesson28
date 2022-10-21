import os
import csv
import requests
import pprint

from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avito.settings')

application = get_wsgi_application()
from ads.models import Location


CREATE_CAT = False
CREATE_AD = False
CREATE_LOCATION = False
CREATE_USER = False


def load_csv_as_dict(path):
    with open(path, mode='r') as f:
        reader = csv.DictReader(f)
        return [x for x in reader]


# cats
if CREATE_CAT:
    json_list = load_csv_as_dict('data/category.csv')
    url = 'http://localhost:8000/cat/create/'
    for item in json_list:
        response = requests.post(
            url=url,
            json={'name': item['name']}
        )
        pprint.pprint(response.json())

url = 'http://localhost:8000/cat/'
response = requests.get(url=url)
pprint.pprint(response.json())


# locations
if CREATE_LOCATION:
    json_list = load_csv_as_dict('data/location.csv')
    for item in json_list:
        Location.objects.create(
            name=item['name'],
            lat=float(item['lat']),
            lng=float(item['lng'])
        )
print(Location.objects.all().values_list())


# users
if CREATE_USER:
    json_list = load_csv_as_dict('data/user.csv')
    url = 'http://localhost:8000/user/create/'
    for item in json_list:
        location = Location.objects.get(id=item['location_id'])
        response = requests.post(
            url=url,
            json={
                'username': item['username'],
                'password': item['password'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'role': item['role'],
                'age': int(item['age']),
                'locations': [location.name, ],
            }
        )
        pprint.pprint(response.json())


url = 'http://localhost:8000/user/'
response = requests.get(url=url)
pprint.pprint(response.json())


if CREATE_AD:
    json_list = load_csv_as_dict('data/ad.csv')
    url = 'http://localhost:8000/ad/create/'
    for item in json_list:
        _is_published = item['is_published']
        is_published = False
        if _is_published == 'TRUE':
            is_published = True
        response = requests.post(
            url=url,
            json={
                'name': item['name'],
                'author_id': int(item['author_id']),
                'price': int(item['price']),
                'description': item['description'],
                'is_published': is_published,
                'image': item['image'],
                'category_id': int(item['category_id']),
            }
        )
        pprint.pprint(response.json())

url = 'http://localhost:8000/ad/'
response = requests.get(url=url)
pprint.pprint(response.json())

url = 'http://localhost:8000/ad/?page=2'
response = requests.get(url=url)
pprint.pprint(response.json())
