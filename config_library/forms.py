from django import forms
from .models import LibraryCollection

class LibraryCollectionForm(forms.ModelForm):
    class Meta:
        model = LibraryCollection
        fields = [ 'collection_name', 'description']
        
        
        

