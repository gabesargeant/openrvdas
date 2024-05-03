from django.contrib import admin

from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'config_library'

urlpatterns = [
    path('', views.index, name='index'),
    path('library', views.library, name='library'),
    path('create_update_transform', views.create_update_transform, name='create_update_transform'),
    path('create_update_transform/<int:transform_id>/', views.create_update_transform, name='create_update_transform'),
    
    path('transforms/', views.transforms, name='transforms'),
    path('transforms/<int:transform_id>/', views.transforms, name='transforms'),
]