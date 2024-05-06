from django.shortcuts import render, redirect
from .forms import LibraryCollectionForm, TransformKVFormSet, TransformsForm, DeleteTransformForm
from .models import LibraryCollection, Transforms, TransformKVStore, Writers
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

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


class RVDASModelKVView(TemplateView):
    template_name = "model_list.html"
    model_name="model"
    model = None
    dmf = None
    model_id = 'model_id'

    def get(self, request, *args, **kwargs):

        all_models = self.model.objects.all()        
        models = []

        for mod in all_models:

            form = self.dmf(initial={self.model_id: getattr(mod, self.model_id)})  
                                  
            models.append({self.model_name: mod, 'delete_form': form})

        return render(request, self.template_name, {self.model_name: models})
    
    def post(self, request, *args, **kwargs):
        
        form = self.dmf(request.POST)
        if form.is_valid():
            transform_id = form.cleaned_data['transform_id']
            transform = Transforms.objects.get(transform_id=transform_id)
            transform.delete()
            TransformKVStore.objects.filter(transform__transform_id=transform_id).delete()
            return redirect('config_library:transforms')  
    



class TransformsView(RVDASModelKVView):
    template_name = "transforms_list.html"
    model_name="transforms"
    model = Transforms
    dmf = DeleteTransformForm #Use the generic one
    model_id = 'transform_id'

class WritersView(RVDASModelKVView):
    template_name = "transforms_list.html"
    model_name="writers"
    model = Writers
    dmf = None
    model_id = 'writer_id'




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
        

