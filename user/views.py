import json
import math

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, UpdateView, CreateView, DetailView, ListView

from ads.models import Location
from user.models import User


class UserListView(ListView):
    model = User
    ordering = 'username'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().prefetch_related('locations')

        total = self.object_list.count()
        page = request.GET.get('page')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)

        items = []
        for item in page_obj:
            locations = [x.name for x in item.locations.all()]
            items.append({
                'id': item.id,
                'username': item.username,
                'first_name': item.first_name,
                'last_name': item.last_name,
                'role': item.role,
                'age': item.age,
                'locations': locations,
                'total_ads': item.ads.filter(is_published=True).aggregate(count=Count('id'))['count']
            })

        response = {
            'total': total,
            'items': items,
            'num_pages': math.ceil(float(total) / settings.TOTAL_ON_PAGE)
        }

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse({
                'id': self.object.id,
                'username': self.object.username,
                'first_name': self.object.first_name,
                'last_name': self.object.last_name,
                'role': self.object.role,
                'age': self.object.age,
                'locations': [x.name for x in self.object.locations.all()]
            })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'age', 'password', 'locations']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
        )

        user.first_name = data['first_name'] if data.get('first_name') else user.first_name
        user.last_name = data['last_name'] if data.get('last_name') else user.last_name
        user.role = data['role'] if data.get('role') else user.role
        user.age = data['age'] if data.get('age') else user.age

        if data.get('locations'):
            for location in data['locations']:
                location_instance, _ = Location.objects.get_or_create(name=location)
                user.locations.add(location_instance)
        user.save()

        return JsonResponse({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'age': user.age,
                'locations': [x.name for x in user.locations.all()]
            }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'age', 'password', 'locations']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.username = data['username'] if data.get('username') else self.object.username
        self.object.first_name = data['first_name'] if data.get('first_name') else self.object.first_name
        self.object.last_name = data['last_name'] if data.get('last_name') else self.object.last_name
        self.object.role = data['role'] if data.get('role') else self.object.role
        self.object.age = data['age'] if data.get('age') else self.object.age

        if data.get('password'):
            self.object.set_password(data['password'])

        if data.get('locations'):
            for location in data['locations']:
                location_instance, _ = Location.objects.get_or_create(name=location)
                self.object.locations.add(location_instance)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)
        self.object.save()

        return JsonResponse({
                'id': self.object.id,
                'username': self.object.username,
                'first_name': self.object.first_name,
                'last_name': self.object.last_name,
                'role': self.object.role,
                'age': self.object.age,
                'locations': [x.name for x in self.object.locations.all()]
            }, status=202)

    def patch(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=200)
