from django.urls import path

from user.views import (
    UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView,
)

urlpatterns = [
    path('user/', UserListView.as_view()),
    path('user/create/', UserCreateView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
    path('user/<int:pk>/update/', UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', UserDeleteView.as_view()),
]
