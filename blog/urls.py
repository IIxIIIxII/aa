from django.urls import path
from . import views

urlpatterns = [
  path('', views.post_list, name='post_list'),
  path('<int:pk>/', views.post_detail, name='post_detail'),
  path('new/', views.post_create, name='post_create'),
  path('<int:pk>/edit', views.post_update, name='post_update'),
  path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
  path('category/<int:category_id>/edit/', views.edit_category, name='edit_category'),
  path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
  path('post/<int:post_pk>/remove_category/<int:category_id>/', views.remove_category_from_post, name='remove_category_from_post'),
]