from django import forms
from .models import LibraryCollection, TransformKVStore, Transforms, TypeChoices

class LibraryCollectionForm(forms.ModelForm):
    class Meta:
        model = LibraryCollection
        fields = [ 'collection_name', 'description']
        

class TransformsForm(forms.ModelForm):
    
    
    class Meta:
        model = Transforms
        fields = ['transform_id', 'name', 'description']

class TransformKVForm(forms.ModelForm):
    class Meta:
        model = TransformKVStore
        fields = ['key', 'value', 'type']
        widgets = {
            "value": forms.TextInput(),
            "key": forms.TextInput(),
        }
        

TransformKVFormSet = forms.inlineformset_factory(
    Transforms, TransformKVStore, form=TransformKVForm, extra=1, min_num=0
)

class DeleteTransformForm(forms.ModelForm):
    transform_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Transforms
        fields = ['transform_id']
        widgets = {
            'transform_id': forms.HiddenInput(),
        }