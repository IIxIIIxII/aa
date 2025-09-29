from django.urls import path
from . import views

urlpatterns = [
  path('', views.post_list, name='post_list'),
  path('<int:pk>/', views.post_detail, name='post_detail'),
  path('new/', views.post_create, name='post_create'),
  path('<int:pk>/edit', views.post_update, name='post_update'),
]