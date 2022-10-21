import json
import math

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from ads.models import Category, Ad


def index(request):
    return JsonResponse({'status': 'ok'}, status=200)


class CategoryListView(ListView):
    model = Category
    ordering = 'name'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        search_text = request.GET.get('name', None)
        if search_text:
            self.object_list = self.object_list.filter(name=search_text)

        total = self.object_list.count()
        page = request.GET.get('page')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)

        items = []
        for item in page_obj:
            items.append({
                'id': item.id,
                'name': item.name,
            })

        response = {
            'total': total,
            'items': items,
            'num_pages': math.ceil(float(total) / settings.TOTAL_ON_PAGE)
        }

        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        cat = Category.objects.create(
            name=data['name'],
        )

        return JsonResponse({
            'id': cat.id,
            'name': cat.name,
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data['name'] if data.get('name') else self.object.name

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
        }, status=202)

    def patch(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().order_by('-price').select_related('author').select_related('category')
        search_text = request.GET.get('name', None)
        if search_text:
            self.object_list = self.object_list.filter(name=search_text)

        total = self.object_list.count()
        page = request.GET.get('page')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page)

        items = []
        for item in page_obj:
            items.append({
                'id': item.id,
                'name': item.name,
                'author_id': item.author.id,
                'price': item.price,
                'description': item.description,
                'category_id': item.category.id,
                'is_published': item.is_published,
                'image': item.image.url if item.image else None
            })

        response = {
            'total': total,
            'items': items,
            'num_pages': math.ceil(float(total)/settings.TOTAL_ON_PAGE)
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        ad = Ad.objects.create(
            name=data['name'],
            author_id=data['author_id'],
            price=data['price'],
            description=data['description'],
            category_id=data['category_id'],
            is_published=data['is_published']
        )

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author_id': ad.author.id,
            'price': ad.price,
            'description': ad.description,
            'category_id': ad.category.id,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None
        }, status=201)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author.id,
            'price': self.object.price,
            'description': self.object.description,
            'category_id': self.object.category.id,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.name = data['name'] if data.get('name') else self.object.name
        self.object.author_id = data['author_id'] if data.get('author_id') else self.object.author.id
        self.object.price = data['price'] if data.get('price') else self.object.price
        self.object.description = data['description'] if data.get('description') else self.object.description
        self.object.is_published = data['is_published'] if data.get('is_published') else self.object.is_published
        self.object.category_id = data['category_id'] if data.get('category_id') else self.object.category.id

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author.id,
            'price': self.object.price,
            'description': self.object.description,
            'category_id': self.object.category.id,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None
        }, status=202)

    def patch(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.FILES.get('image'):
            self.object.image = request.FILES['image']
            self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author.id,
            'price': self.object.price,
            'description': self.object.description,
            'category_id': self.object.category.id,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None
        }, status=202)

    def patch(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=200)
