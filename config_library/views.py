from django.shortcuts import render, redirect
from django.http import QueryDict
from .forms import LibraryCollectionForm, ConfigObjectStoreForm
from django.urls import reverse
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
    CountTransformForm,
   DeltaTransformForm,
ExtractFieldTransformForm,
FormatTransformForm,
FromJsonTransformForm,
GeofenceTransformForm,
MaxMinTransformForm,
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
UniqueTransformForm,
ValueFilterTransformForm,
XmlAggregatorTransformForm,
#Complex Forms
InterpolationTransformForm,
InterpolationFieldSpecForm

)
from django import forms

import json

import yaml

class_form_dict = {    
    "DatabaseReader": DatabaseReaderForm,
    "LogFileReader": LogFileReaderForm,
    "ModbusReader": ModbusReaderForm,
    "MqttReader": MqttReaderForm,
    "PolledSerialReader": PolledSerialReaderForm,
    "RedisReader": RedisReaderForm,
    "SerialReader": SerialReaderForm,
    "TcpReader": TcpReaderForm,
    "TextFileReader": TextFileReaderForm,
    "TimeoutReader": TimeoutReaderForm,
    "UdpReader": UdpReaderForm,
    "WebsocketReader": WebsocketReaderForm,
    #Transforms
    "CountTransform": CountTransformForm,
    "DeltaTransform": DeltaTransformForm,
    "ExtractFieldTransform": ExtractFieldTransformForm,
    "FormatTransform": FormatTransformForm,
    "FromJsonTransform": FromJsonTransformForm,
    "GeofenceTransform": GeofenceTransformForm,
    "MaxMinTransform": MaxMinTransformForm,
    "ParseNmeaTransform": ParseNmeaTransformForm,
    "ParseTransform": ParseTransformForm,
    "PrefixTransform": PrefixTransformForm,
    "QcFilterTransform": QcFilterTransformForm,
    "RegexFilterTransform": RegexFilterTransformForm,
    "RegexReplaceTransform": RegexReplaceTransformForm,
    "SliceTransform": SliceTransformForm,
    "SplitTransform": SplitTransformForm,
    "StripTransform": StripTransformForm,
    "TimestampTransform": TimestampTransformForm,
    "ToDasRecordTransform": ToDasRecordTransformForm,
    "ToJsonTransform": ToJsonTransformForm,
    "UniqueTransform": UniqueTransformForm,
    "ValueFilterTransform": ValueFilterTransformForm,
    "XmlAggregatorTransform": XmlAggregatorTransformForm,
}


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


class RVDASConfigObjects(TemplateView):
    template_name = "config_objects.html"
    def get(self, request):
        config_objects = ConfigObjectStore.objects.order_by('-creation_time').all()

        return render(request, self.template_name, {"config_objects": config_objects})
        

class BaseKwargsFormView(TemplateView):
    #
    # This is the basic form view for simple objects that feature a class with kwargs
    # more complicated classes require their own forms.
    #    
    template_name = "kwargs_form.html"
    kwargs_form = None
    name = None

    def get(self, request, *args, **kwargs):

        class_name = kwargs.get('class_name')
        self.kwargs_form = class_form_dict[class_name]
        self.name = class_name
        
        #attempt object lookup
        id = kwargs.get('id', None)
        if id is not None:
            config_object = get_object_or_404(ConfigObjectStore, id=id)

            json_object = config_object.json_object
            py_object_json = json.loads(json_object)

            #unpack #I hate yaml
            #we take the kwargs nested dict and merge it same level as the class name etc.
            initial_form = {
                'class_name':py_object_json['class'],
                'name':py_object_json['name'],
                'id': id,
                'description': config_object.description,
            }
            initial_form.update(py_object_json.get('kwargs', {}))

            form = self.kwargs_form(initial=initial_form)
            post_form = ConfigObjectStoreForm(instance=config_object)


            object_json = json.dumps(py_object_json, default=str, indent=2)
            object_yaml = yaml.dump(py_object_json, sort_keys=False)

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

        # standard GET request.       
        form = self.kwargs_form()
        return render(request, self.template_name, {"name": self.name, "form": form, 'id': id})

    def post(self, request, *args, **kwargs):
        class_name = kwargs.get('class_name')
        self.kwargs_form = class_form_dict[class_name]
        self.name = class_name

        form = self.kwargs_form(request.POST)

        object = {}
        kwargs = {}

        if form.is_valid():

            object = {}
            kwargs = {}
            class_name = None
            for k, v in form.cleaned_data.items():
                if k.lower() == "name":
                    object[k] = v
                elif k.lower() == "object_class":
                    object["class"] = v
                    class_name = v
                elif k.lower() == 'id':
                    object["ObjectStoreId"] = v
                    #print the object id in the yaml/json for tracing.
                elif k.lower() == 'description':
                    #Skip the description. Though maybe something to include?
                    continue
                else:
                    if v is not None:
                        kwargs[k] = v

            if len(kwargs) > 0:
                object["kwargs"] = kwargs

            object_json = json.dumps(object, default=str, indent=2)
                        
            instance_id = form.cleaned_data.get('id')
            print(instance_id)
            try:
                if instance_id is not None:
                    instance_id = int(instance_id)
                    obj = ConfigObjectStore.objects.get(id=instance_id)
                else:
                    raise ValueError("Instance ID is None")
            except (ValueError, ConfigObjectStore.DoesNotExist):
                obj = ConfigObjectStore()
                        
            obj.description = form.cleaned_data.get('description')
            obj.json_object = object_json
            obj.class_name = class_name
            obj.name = form.cleaned_data.get('name')
            obj.save()
            obj_id = obj.id

            return redirect('config_library:config', class_name=class_name, id=obj_id)
        return redirect('config_library:config')

               


        


#
#
# CDR is a complex form, featuring a formset. 
# It's implementation is simmilar to the main KWARGS form.
# ie the same get -> patch/preview -> post request cycle.
#

class CachedDataReaderView(TemplateView):

    template_name = "readers/reader_form_cdr.html"
    name = "CachedDataReader"

    def get(self, request, *args, **kwargs):
        form = CachedDataReaderForm()
        subscription_formset = forms.formset_factory(SubscriptionFields, extra=1, min_num=1
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
        subscription_formset = forms.formset_factory(SubscriptionFields, extra=1, min_num=0)

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
                "name": object.get("name", None),
                "class_name": object.get("class", None),
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




#
#
# Interpolation is a complex form, featuring a formset. 
# It's implementation is simmilar to the main KWARGS form.
# 
#
class InterpolationTransformView(TemplateView):

    template_name = "transforms/complex_transform.html"
    name = "InterpolationTransform"

    fieldset_prefix = 'field_spec'

    def get(self, request, *args, **kwargs):

        id = kwargs.get('id', None)
        if id is not None:
            config_object = get_object_or_404(ConfigObjectStore, id=id)
            post_form = ConfigObjectStoreForm(instance=config_object)

            json_object = config_object.json_object
            py_object_json = json.loads(json_object)
            
            #unpacking everything. Terrible.            
            initial_form = {
                'class_name':py_object_json['class'],
                'name':py_object_json['name'],
                'id': id,
                'description': config_object.description,
                **py_object_json['kwargs']
            }
            form = InterpolationTransformForm(initial=initial_form)

            intial_formset_data = []
            for k,v in py_object_json['kwargs']['field_spec'].items():                
                intial_formset_data.append( {
                    'interpolated_field':k,
                    'source' : v['source'],
                    **v['algorithm'],
                  
                })


            
            field_spec_formset = forms.formset_factory(InterpolationFieldSpecForm,extra=1, min_num=0)            
            formset = field_spec_formset(prefix=self.fieldset_prefix, initial=intial_formset_data)

            object_json = json.dumps(py_object_json, default=str, indent=2)
            object_yaml = yaml.dump(py_object_json, sort_keys=False)

            return render(
                request,
                self.template_name,
                {
                    "name": self.name,
                    "form": form,
                      "formsets": [
                    {"name": self.fieldset_prefix, "formset": formset},
                ],
                    "json_object": object_json,
                    "yaml_object": object_yaml,
                    "post_form": post_form,
                    
                },
            )            

        form = InterpolationTransformForm()
        field_spec_formset = forms.formset_factory(InterpolationFieldSpecForm,
             extra=1, min_num=0
        )
        field_spec_formset = field_spec_formset(prefix=self.fieldset_prefix)

        return render(
            request,
            self.template_name,
            {
                "name": self.name,
                "form": form,
                "formsets": [
                    {"name": self.fieldset_prefix, "formset": field_spec_formset},
                ],
            },
        )

    def post(self, request, *args, **kwargs):

        form = InterpolationTransformForm(request.POST, request.FILES)
        field_spec_formset = forms.formset_factory(form=InterpolationFieldSpecForm, extra=1, min_num=0)
        formset = field_spec_formset(request.POST, prefix=self.fieldset_prefix)
        
        object = {}
        kwargs = {}

        if form.is_valid() and formset.is_valid():            
            class_name = None       
            for k, v in form.cleaned_data.items():
                if k.lower() == "name":
                    object[k] = v
                elif k.lower() == "object_class":
                    object["class"] = v
                    class_name = v
                elif k.lower() == 'id':
                    object["ObjectStoreId"] = v
                    #print the object id in the yaml/json for tracing.
                elif k.lower() == 'description':
                    #Skip the description. Though maybe something to include?
                    continue
                else:
                    if v is not None:
                        kwargs[k] = v

            kwargs['field_spec'] = {}
            object["kwargs"] = kwargs
            #Don't blame me, complex forms are complex.
            field_spec = {}
            
            for subform in formset:
                sf = subform.cleaned_data                                
                interpolated_field = sf.get('interpolated_field', None)
                if interpolated_field is None:
                    continue
            
                field_spec_instance = {
                    'source': sf.get('source', None), 
                    'algorithm':{
                    'type': sf.get('type',None), 
                    'window': sf.get('window', None),
                    }
                }
                field_spec[interpolated_field] = field_spec_instance
            
            object["kwargs"]["field_spec"] = field_spec
            
            object_json = json.dumps(object, default=str, indent=2)       
            instance_id = form.cleaned_data.get('id')
            try:
                if instance_id is not None:
                    instance_id = int(instance_id)
                    obj = ConfigObjectStore.objects.get(id=instance_id)
                else:
                    raise ValueError("Instance ID is None")
            except (ValueError, ConfigObjectStore.DoesNotExist):
                obj = ConfigObjectStore()
                        
            obj.description = form.cleaned_data.get('description')
            obj.json_object = object_json
            obj.class_name = class_name
            obj.name = form.cleaned_data.get('name')
            obj.save()
            obj_id = obj.id

        
            return redirect('config_library:config', class_name=class_name, id=obj_id)
        return redirect('config_library:config')

