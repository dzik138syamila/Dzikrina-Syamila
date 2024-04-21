# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('posts/', views.post_list, name='post_list'),
    path('pages/', views.page_list, name='page_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]
