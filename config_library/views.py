from django.shortcuts import render, redirect
from .forms import (
    LibraryCollectionForm,
    TransformKVFormSet,
    TransformsForm,
    DeleteTransformForm,
)
from .models import LibraryCollection, Transforms, TransformKVStore, Writers
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
    ReaderForm,
    RedisReaderForm,
    SerialReaderForm,
    TcpReaderForm,
    TextFileReaderForm,
    TimeoutReaderForm,
    UdpReaderForm,
    WebsocketReaderForm
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


class CachedDataReader(TemplateView):
    template_name = "reader_form_cdr.html"

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

        # POST, grab the object data data,
        # construct the json object

    def patch(self, request, *args, **kwargs):
        form = CachedDataReaderForm(request.POST, request.FILES)
        subscription_formset = forms.formset_factory(form=SubscriptionFields)
        formset = subscription_formset(request.POST, prefix="subscription")

        object = {}
        kwargs = {}
        if form.is_valid() and formset.is_valid():

            object = {"class": form.cleaned_data.get("object_class", None)}
            kwargs = {
                "data_server": form.cleaned_data.get("data_server", None),
                "use_wss": form.cleaned_data.get("use_wss"),
                "check_cert": form.cleaned_data.get("check_cert"),
                "subscription": {},
            }
            object["kwargs"] = kwargs

        fields = {}
        for f in formset:
            fields.update(
                {
                    f.cleaned_data.get("field"): {
                        "seconds": f.cleaned_data.get("seconds")
                    }
                }
            )

        kwargs["subscription"]["fields"] = fields

        import json
        import yaml

        object_json = json.dumps(object, default=str, indent=2)
        object_yaml = yaml.dump(object)

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
            },
        )


# Base view
class ReaderFormView(TemplateView):
    template_name = "reader_form.html"
    reader_form = None

    def get(self, request, *args, **kwargs):
        # Handle the lookup.

        form = self.reader_form()

        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):

        method = self.request.POST.get("_method", "").lower()
        if method == "patch":
            return self.patch(request, *args, **kwargs)

        # POST, grab the object data data,
        # construct the json object

    def patch(self, request, *args, **kwargs):
        form = self.reader_form(request.POST)

        object = {}
        kwargs = {}
        if form.is_valid():

            object = {}
            kwargs = {}

            for k, v in form.cleaned_data.items():
                if k.lower() == "name" or k.lower() == "object_class":
                    object[k] = v
                else:
                    kwargs[k] = v

        object_json = json.dumps(object, default=str, indent=2)
        object_yaml = yaml.dump(object)

        return render(
            request,
            self.template_name,
            {"form": form, "json_object": object_json, "yaml_object": object_yaml},
        )


class DatabaseReaderView(ReaderFormView):
    reader_form = DatabaseReaderForm


class LogFileReaderView(ReaderFormView):
    reader_form = LogFileReaderForm


class ModbusReaderView(ReaderFormView):
    reader_form = ModbusReaderForm


class MqttReaderView(ReaderFormView):
    reader_form = MqttReaderForm


class PolledSerialReaderView(ReaderFormView):
    reader_form = PolledSerialReaderForm


class ReaderView(ReaderFormView):
    reader_form = ReaderForm


class RedisReaderView(ReaderFormView):
    reader_form = RedisReaderForm


class SerialReaderView(ReaderFormView):
    reader_form = SerialReaderForm


class TcpReaderView(ReaderFormView):
    reader_form = TcpReaderForm


class TextFileReaderView(ReaderFormView):
    reader_form = TextFileReaderForm


class TimeoutReaderView(ReaderFormView):
    reader_form = TimeoutReaderForm


class UdpReaderView(ReaderFormView):
    reader_form = UdpReaderForm

class WebsocketReaderView(ReaderFormView):
    reader_form = WebsocketReaderForm
