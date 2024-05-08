from django.shortcuts import render, redirect
from .forms import LibraryCollectionForm, TransformKVFormSet, TransformsForm, DeleteTransformForm
from .models import LibraryCollection, Transforms, TransformKVStore, Writers
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .reader_forms import CachedDataReaderForm, SubscriptionFields
from django import forms
def index(request):    
    return render(request, 'index.html', {})

def library(request):
    if request.method == 'POST':
        form = LibraryCollectionForm(request.POST)
        if form.is_valid():
            form.save()        
            return redirect('config_library:library')
    else:
        form = LibraryCollectionForm()

    collections = LibraryCollection.objects.all()
    return render(request, 'library.html', {'form': form, "collections": collections})


class TransformsView(TemplateView):
    template_name = "transforms_list.html"
    def get(self, request, *args, **kwargs):

        transforms = Transforms.objects.all()        
        result = []

        for t in transforms:
            form = DeleteTransformForm(initial={'transform_id': t.transform_id})                                    
            result.append({'transforms': t, 'delete_form': form})

        print(result)
        return render(request, self.template_name, {'transforms': result})
    
    def post(self, request, *args, **kwargs):
        
        form = self.dmf(request.POST)
        if form.is_valid():
            transform_id = form.cleaned_data['transform_id']
            transform = Transforms.objects.get(transform_id=transform_id)
            transform.delete()
            TransformKVStore.objects.filter(transform__transform_id=transform_id).delete()
            return redirect('config_library:transforms')  
    

class TransformView(TemplateView):
    #View Edit or Author a SINGLE Transform.
    
    template_name = "transform.html"

    def get(self, request, *args, **kwargs):
        transform_id = kwargs.get('transform_id', None)
        if transform_id is None:
            form = TransformsForm()
            formset = TransformKVFormSet()
        else:
            transform = get_object_or_404(Transforms, transform_id=transform_id)
            
            # Initialize the TransformForm with the instance of Transform
            form = TransformsForm(instance=transform)
            
            # Query the related TransformKVStore objects for the given Transform
            transform_kv = TransformKVStore.objects.filter(transform_id=transform.transform_id)
            
            # formset = TransformKVFormSet(queryset=transform_kv)
            # Initialize the formset with the queryset
            formset = TransformKVFormSet(queryset=transform_kv, instance=transform)


            




        return render(request, self.template_name, {'form': form, 'formset': formset})
    
    def post(self, request, *args, **kwargs):       
        
        transform_id = kwargs.get('transform_id', None)

        if transform_id is not None:
            instance =  get_object_or_404(Transforms, transform_id=transform_id)
            form = TransformsForm(request.POST, instance=instance)
            formset = TransformKVFormSet(request.POST, instance=instance)
        else:
            instance =  Transforms.objects.create()
            form = TransformsForm(request.POST, instance=instance)
            formset = TransformKVFormSet(request.POST, instance=instance)
            transform_id = instance.transform_id
                
        if form.is_valid() and formset.is_valid():
        
            transform = form.save(commit=False)
            transform.save()
            formset.save(commit=False)
        
            for formset_instance in formset:
                if any(formset_instance.cleaned_data):
                    if 'DELETE' in formset_instance.cleaned_data and formset_instance.cleaned_data['DELETE'] == True:
                        formset_instance.instance.delete()                    
                        continue                   

                    instance = formset_instance.instance
                    instance.transform = transform  # Set the foreign key relationship
                    instance.save()  # Save the related object

            formset.save(commit=True)

            return redirect('config_library:transform', transform_id=transform_id)  # Redirect to a success URL
        else:
            #form is not valid
            # print(form.errors)
            # print(formset.errors)
            return render(request, self.template_name, {'form': form, 'formset':formset})
        

class CachedDataReader(TemplateView):
    template_name = "reader_form.html"
    def get(self, request, *args, **kwargs):
        form = CachedDataReaderForm()
        subscription_formset = forms.formset_factory(SubscriptionFields)
        subscription = subscription_formset(prefix='subscription')

        return render(request, 
                      self.template_name, 
                      {'form': form, 'formsets':[
                          {'name': 'subscription', 'formset': subscription},
                          ]})

    def post(self, request, *args, **kwargs):

        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch( request, *args, **kwargs)
        

    def patch(self, request, *args, **kwargs):
        form = CachedDataReaderForm(request.POST, request.FILES)
        subscription_formset = forms.formset_factory(form=SubscriptionFields)
        formset = subscription_formset(request.POST, prefix="subscription")

        object = {}
        kwargs = {}
        if form.is_valid() and formset.is_valid():

            object = {'class': form.cleaned_data.get('object_class', None)}
            kwargs = {                      
                      'data_server': form.cleaned_data.get('data_server', None),
                      'use_wss': form.cleaned_data.get('use_wss'),
                      'check_cert': form.cleaned_data.get('check_cert'),
                      'fields': {}
                      }
            object['kwargs'] = kwargs

        fields = {}
        for f in formset:                            
                fields.update({f.cleaned_data.get('field'): {"seconds": f.cleaned_data.get('seconds') }})
                
        kwargs['fields'] = fields
        

        import json
        import yaml
        object_json = json.dumps(object, default=str, indent=2)
        object_yaml = yaml.dump(object)

        return render(request, 
                      self.template_name, 
                      {'form': form, 'formsets':[
                          {'name': 'subscription', 'formset': formset},
                          ],
                        'json_object':object_json,
                        'yaml_object':object_yaml
                        })

        

