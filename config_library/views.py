from django.shortcuts import render, redirect
from .forms import LibraryCollectionForm, TransformKVFormSet, TransformsForm
from .models import LibraryCollection, Transforms, TransformKVStore
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


def create_update_transform(request, transform_id=None):

    if request.method == 'POST':
        
        if transform_id is not None:
            instance =  get_object_or_404(Transforms, transform_id=transform_id)
            form = TransformsForm(request.POST, instance=instance)
            formset = TransformKVFormSet(request.POST, instance=instance)
        else:
            form = TransformsForm(request.POST)        
            formset = TransformKVFormSet(request.POST)
            
        
        
        if form.is_valid() and formset.is_valid():
        
            transform = form.save(commit=False)
            transform.save()
            formset.save(commit=False)
        
            for form_instance in formset:
                print(form_instance.cleaned_data)
                if 'DELETE' in form_instance.cleaned_data and form_instance.cleaned_data['DELETE'] == True:
                    form_instance.instance.delete()
                    continue
               
                instance = form_instance.instance
                instance.transform = transform  # Set the foreign key relationship
                instance.save()  # Save the related object

            formset.save_m2m()
        
            return redirect('config_library:create_update_transform', transform_id=transform_id)  # Redirect to a success URL
        else:
            print(form.errors)
            print(formset.errors)
    else: #GET
        if transform_id is not None:
            transform = get_object_or_404(Transforms, transform_id=transform_id)
            
            # Initialize the TransformForm with the instance of Transform
            form = TransformsForm(instance=transform)
            
            # Query the related TransformKVStore objects for the given Transform
            transform_kv = TransformKVStore.objects.filter(transform_id=transform.transform_id)
            
            # formset = TransformKVFormSet(queryset=transform_kv)
            # Initialize the formset with the queryset
            formset = TransformKVFormSet(queryset=transform_kv, instance=transform)
        else:
            form = TransformsForm()
            formset = TransformKVFormSet()

    return render(request, 'transforms.html', {'form': form, 'formset': formset})

#Get only, Displays a Transform.
def transforms(request, transform_id = None):

    

    if transform_id is None:
        all_transforms = Transforms.objects.all()
    else:
    
        transform = Transforms.objects.get(transform_id=transform_id)  # Replace my_transform_id with the actual ID
        transform_kvs = transform.key_values.all()
        transform = {
            "transform": transform,
            "tkv": transform_kvs
        }


    return render(request, 'transforms_view.html', {"all_transforms": all_transforms})
    

