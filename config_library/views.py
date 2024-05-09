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
from django.urls import include, path
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
class ReaderFormView(TemplateView):
    template_name = "reader_form.html"
    reader_form = None
    name = None

    def get(self, request, *args, **kwargs):
        # Handle the lookup.

        form = self.reader_form()

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
        form = self.reader_form(request.POST)

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


class DatabaseReaderView(ReaderFormView):
    reader_form = DatabaseReaderForm
    name = "DatabaseReader"


class LogFileReaderView(ReaderFormView):
    reader_form = LogFileReaderForm
    name = "LogFileReader"


class ModbusReaderView(ReaderFormView):
    reader_form = ModbusReaderForm
    name = "ModbusReader"


class MqttReaderView(ReaderFormView):
    reader_form = MqttReaderForm
    name = "MqttReader"


class PolledSerialReaderView(ReaderFormView):
    reader_form = PolledSerialReaderForm
    name = "PolledSerialReader"


class RedisReaderView(ReaderFormView):
    reader_form = RedisReaderForm
    name = "RedisReader"


class SerialReaderView(ReaderFormView):
    reader_form = SerialReaderForm
    name = "SerialReader"


class TcpReaderView(ReaderFormView):
    reader_form = TcpReaderForm
    name = "TcpReader"


class TextFileReaderView(ReaderFormView):
    reader_form = TextFileReaderForm
    name = "TextFileReader"


class TimeoutReaderView(ReaderFormView):
    reader_form = TimeoutReaderForm
    name = "TimeoutReader"


class UdpReaderView(ReaderFormView):
    reader_form = UdpReaderForm
    name = "UdpReader"


class WebsocketReaderView(ReaderFormView):
    reader_form = WebsocketReaderForm
    name = "WebsocketReader"
