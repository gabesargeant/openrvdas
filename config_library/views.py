from django.shortcuts import render, redirect
from .forms import LibraryCollectionForm, TransformKVFormSet, TransformsForm
from .models import LibraryCollection


def index(request):    
    return render(request, 'index.html', {})

def library(request):
    if request.method == 'POST':
        form = LibraryCollectionForm(request.POST)
        if form.is_valid():
            form.save()        
            return redirect('library')
    else:
        form = LibraryCollectionForm()

    collections = LibraryCollection.objects.all()
    return render(request, 'library.html', {'form': form, "collections": collections})


def transforms(request):
    if request.method == 'POST':
        form = TransformsForm(request.POST)
        formset = TransformKVFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            transform = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.transform = transform
                instance.save()
            return redirect('transforms')  # Redirect to a success URL
    else:
        form = TransformsForm()
        formset = TransformKVFormSet()
    return render(request, 'transforms.html', {'form': form, 'formset': formset})
