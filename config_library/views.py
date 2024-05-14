from django.shortcuts import render, redirect
from .forms import LibraryCollectionForm, ConfigObjectStoreForm

from .models import LibraryCollection, ConfigObjectStore
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .reader_forms import (
    CachedDataReaderForm,
    SubscriptionFields,
    DatabaseReaderForm,
    LogFileReaderForm,
    ModbusReaderForm,
    MqttReaderForm,
    PolledSerialReaderForm,
    RedisReaderForm,
    SerialReaderForm,
    TcpReaderForm,
    TextFileReaderForm,
    TimeoutReaderForm,
    UdpReaderForm,
    WebsocketReaderForm,
)
from .transform_forms import (
   DeltaTransformForm,
ExtractFieldTransformForm,
FormatTransformForm,
FromJsonTransformForm,
GeofenceTransformForm,
ParseNmeaTransformForm,
ParseTransformForm,
PrefixTransformForm,
QcFilterTransformForm,
RegexFilterTransformForm,
RegexReplaceTransformForm,
SliceTransformForm,
SplitTransformForm,
StripTransformForm,
TimestampTransformForm,
ToDasRecordTransformForm,
ToJsonTransformForm,
ValueFilterTransformForm,
XmlAggregatorTransformForm,
)
from django import forms

import json

import yaml


def index(request):
    return render(request, "index.html", {})


def library(request):
    if request.method == "POST":
        form = LibraryCollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("config_library:library")
    else:
        form = LibraryCollectionForm()

    collections = LibraryCollection.objects.all()
    return render(request, "library.html", {"form": form, "collections": collections})







class CachedDataReaderView(TemplateView):

    template_name = "reader_form_cdr.html"
    name = "CachedDataReader"

    def get(self, request, *args, **kwargs):
        form = CachedDataReaderForm()
        subscription_formset = forms.formset_factory(
            SubscriptionFields, extra=1, min_num=0
        )
        subscription = subscription_formset(prefix="subscription")

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "formsets": [
                    {"name": "subscription", "formset": subscription},
                ],
            },
        )

    def post(self, request, *args, **kwargs):

        method = self.request.POST.get("_method", "").lower()
        if method == "patch":
            return self.patch(request, *args, **kwargs)

        form = ConfigObjectStoreForm(request.POST)
        if form.is_valid():
            form.save()
        
        return redirect('config_library:index')

    def patch(self, request, *args, **kwargs):
        form = CachedDataReaderForm(request.POST, request.FILES)
        subscription_formset = forms.formset_factory(form=SubscriptionFields)
        formset = subscription_formset(request.POST, prefix="subscription")

        object = {}
        kwargs = {}
        if form.is_valid() and formset.is_valid():
            
            for k, v in form.cleaned_data.items():
                if k.lower() == "name":
                    object[k] = v
                elif k.lower() == "object_class":
                    object["class"] = v
                else:
                    if v is not None:
                        kwargs[k] = v

            kwargs['subscription'] = {}
            object["kwargs"] = kwargs
            #Don't blame me, blame the subscription object on the cached data reader.
            fields = {}
            for subform in formset:
                sf = subform.cleaned_data                                
                if sf['field'] is not None:
                    fields[sf['field']] = {'seconds': sf['seconds']}
            
            print(object)
            object["kwargs"]["subscription"]["fields"] = fields

        object_json = json.dumps(object, default=str, indent=2)
        object_yaml = yaml.dump(object, sort_keys=False)

        # Creat the submission Initial Form (this is the object store, use to add description.)
        post_form = ConfigObjectStoreForm(
            initial={
                "name": object["name"],
                "class_name": object["class"],
                "description": "",
                "json_object": object_json,
            }
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "formsets": [
                    {"name": "subscription", "formset": formset},
                ],
                "json_object": object_json,
                "yaml_object": object_yaml,
                "post_form": post_form,
            },
        )


# Base view
class BaseKwargsFormView(TemplateView):
    #
    # These three attributes usually get overridden.
    #    
    template_name = "kwargs_form.html"
    kwargs_form = None
    name = None

    def get(self, request, *args, **kwargs):
        # Handle the lookup.

        form = self.kwargs_form()

        return render(request, self.template_name, {"name": self.name, "form": form})

    def post(self, request, *args, **kwargs):

        method = self.request.POST.get("_method", "").lower()
        if method == "patch":
            return self.patch(request, *args, **kwargs)


        form = ConfigObjectStoreForm(request.POST)
        if form.is_valid():
            form.save()
        
        return redirect('config_library:index')



    def patch(self, request, *args, **kwargs):
        form = self.kwargs_form(request.POST)

        object = {}
        kwargs = {}
        if form.is_valid():

            object = {}
            kwargs = {}

            for k, v in form.cleaned_data.items():
                if k.lower() == "name":
                    object[k] = v
                elif k.lower() == "object_class":
                    object["class"] = v
                else:
                    if v is not None:
                        kwargs[k] = v

            object["kwargs"] = kwargs

        object_json = json.dumps(object, default=str, indent=2)
        object_yaml = yaml.dump(object, sort_keys=False)

        # Creat the submission Initial Form
        post_form = ConfigObjectStoreForm(
            initial={
                "name": object["name"],
                "class_name": object["class"],
                "description": "",
                "json_object": object_json,
            }
        )

        return render(
            request,
            self.template_name,
            {
                "name": self.name,
                "form": form,
                "json_object": object_json,
                "yaml_object": object_yaml,
                "post_form": post_form,
            },
        )


class DatabaseReaderView(BaseKwargsFormView):
    kwargs_form = DatabaseReaderForm
    name = "DatabaseReader"


class LogFileReaderView(BaseKwargsFormView):
    kwargs_form =  LogFileReaderForm
    name = "LogFileReader"


class ModbusReaderView(BaseKwargsFormView):
    kwargs_form =  ModbusReaderForm
    name = "ModbusReader"


class MqttReaderView(BaseKwargsFormView):
    kwargs_form =  MqttReaderForm
    name = "MqttReader"


class PolledSerialReaderView(BaseKwargsFormView):
    kwargs_form =  PolledSerialReaderForm
    name = "PolledSerialReader"


class RedisReaderView(BaseKwargsFormView):
    kwargs_form =  RedisReaderForm
    name = "RedisReader"


class SerialReaderView(BaseKwargsFormView):
    kwargs_form =  SerialReaderForm
    name = "SerialReader"


class TcpReaderView(BaseKwargsFormView):
    kwargs_form =  TcpReaderForm
    name = "TcpReader"


class TextFileReaderView(BaseKwargsFormView):
    kwargs_form =  TextFileReaderForm
    name = "TextFileReader"


class TimeoutReaderView(BaseKwargsFormView):
    kwargs_form =  TimeoutReaderForm
    name = "TimeoutReader"


class UdpReaderView(BaseKwargsFormView):
    kwargs_form =  UdpReaderForm
    name = "UdpReader"


class WebsocketReaderView(BaseKwargsFormView):
    kwargs_form =  WebsocketReaderForm
    name = "WebsocketReader"


#
#
# TRANSFORMS
#
#


class DeltaTransformView(BaseKwargsFormView):
    kwargs_form =  DeltaTransformForm
    name = "DeltaTransform"

class ExtractFieldTransformView(BaseKwargsFormView):
    kwargs_form =  ExtractFieldTransformForm
    name = "ExtractFieldTransform"

class FormatTransformView(BaseKwargsFormView):
    kwargs_form =  FormatTransformForm
    name = "FormatTransform"

class FromJsonTransformView(BaseKwargsFormView):
    kwargs_form =  FromJsonTransformForm
    name = "FromJsonTransform"
class GeofenceTransformView(BaseKwargsFormView):
    kwargs_form =  GeofenceTransformForm
    name = "GeofenceTransform"

class ParseNmeaTransformView(BaseKwargsFormView):
    kwargs_form =  ParseNmeaTransformForm
    name = "ParseNmeaTransform"

class ParseTransformView(BaseKwargsFormView):
    kwargs_form =  ParseTransformForm
    name = "ParseTransform"

class PrefixTransformView(BaseKwargsFormView):
    kwargs_form =  PrefixTransformForm
    name = "PrefixTransform"

class QcFilterTransformView(BaseKwargsFormView):
    kwargs_form =  QcFilterTransformForm
    name = "QcFilterTransform"

class RegexFilterTransformView(BaseKwargsFormView):
    kwargs_form =  RegexFilterTransformForm
    name = "RegexFilterTransform"

class RegexReplaceTransformView(BaseKwargsFormView):
    kwargs_form =  RegexReplaceTransformForm
    name = "RegexReplaceTransform"

class SliceTransformView(BaseKwargsFormView):
    kwargs_form =  SliceTransformForm
    name = "SliceTransform"

class SplitTransformView(BaseKwargsFormView):
    kwargs_form =  SplitTransformForm
    name = "SplitTransform"

class StripTransformView(BaseKwargsFormView):
    kwargs_form =  StripTransformForm
    name = "StripTransform"

class TimestampTransformView(BaseKwargsFormView):
    kwargs_form =  TimestampTransformForm
    name = "TimestampTransform"

class ToDasRecordTransformView(BaseKwargsFormView):
    kwargs_form =  ToDasRecordTransformForm
    name = "ToDasRecordTransform"

class ToJsonTransformView(BaseKwargsFormView):
    kwargs_form =  ToJsonTransformForm
    name = "ToJsonTransform"

class ValueFilterTransformView(BaseKwargsFormView):
    kwargs_form =  ValueFilterTransformForm
    name = "ValueFilterTransform"

class XmlAggregatorTransformView(BaseKwargsFormView):
    kwargs_form =  XmlAggregatorTransformForm
    name = "XmlAggregatorTransform"