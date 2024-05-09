from django import forms
from .models import LibraryCollection, ConfigObjectStore

class LibraryCollectionForm(forms.ModelForm):
    class Meta:
        model = LibraryCollection
        fields = [ 'collection_name', 'description']
        

class ConfigObjectStoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #fields read-only
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['class_name'].widget.attrs['readonly'] = True
        self.fields['json_object'].widget.attrs['readonly'] = True
    class Meta:
        model = ConfigObjectStore
        fields = ['name', 'description', 'class_name', 'json_object']