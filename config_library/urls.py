from django.contrib import admin

from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = "config_library"

urlpatterns = [
    path("", views.index, name="index"),
    path("library", views.library, name="library"),
    path("rvdas_config_objects", views.RVDASConfigObjects.as_view(), name="rvdas_config_objects"),
    # Complex Readers
    path("config/CachedDataReader/", views.CachedDataReaderView.as_view(), name="cached_data_reader"),
    path("config/CachedDataReader/<id>", views.CachedDataReaderView.as_view(), name="cached_data_reader"),
    path("config/InterpolationTransform/", views.InterpolationTransformView.as_view(), name="interpolation_transform_view"),
    path("config/InterpolationTransform/<id>", views.InterpolationTransformView.as_view(), name="interpolation_transform_view"),
    # KWARG Forms, this is the most generic case and needs to be at the end to match AFTER special cases have been scanned.
    path("config/<class_name>/", views.BaseKwargsFormView.as_view(), name="config"),
    path("config/<class_name>/<id>", views.BaseKwargsFormView.as_view(), name="config"),
]
