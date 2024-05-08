from django.contrib import admin

from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'config_library'

urlpatterns = [
    path('', views.index, name='index'),
    path('library', views.library, name='library'),
    
    
    #List transforms
    path('transforms/', views.TransformsView.as_view(), name='transforms'),
    
    #Edit single transform
    path('transform/', views.TransformView.as_view(), name='transform'),
    path('transform/<int:transform_id>/', views.TransformView.as_view(), name='transform'),
    #reader form
    path('readers/cached_data_reader/', views.CachedDataReader.as_view(), name='cached_data_reader'),
    
]