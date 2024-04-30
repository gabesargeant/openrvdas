from django.shortcuts import render, redirect
from .forms import LibraryCollectionForm
from .models import LibraryCollection


def index():
    #list the libraries

    pass

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