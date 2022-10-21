from django.urls import path

from ads.views import (
    CategoryListView, CategoryCreateView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView,
    AdDetailView, AdListView, AdCreateView, AdUpdateView, AdDeleteView, AdUploadImageView
)

urlpatterns = [
    # Category
    path('cat/', CategoryListView.as_view()),
    path('cat/create/', CategoryCreateView.as_view()),
    path('cat/<int:pk>/', CategoryDetailView.as_view()),
    path('cat/<int:pk>/update/', CategoryUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view()),

    # Ad
    path('ad/', AdListView.as_view()),
    path('ad/create/', AdCreateView.as_view()),
    path('ad/<int:pk>/', AdDetailView.as_view()),
    path('ad/<int:pk>/update/', AdUpdateView.as_view()),
    path('ad/<int:pk>/upload_image/', AdUploadImageView.as_view()),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view()),

]
