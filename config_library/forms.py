from django import forms
from .models import LibraryCollection, TransformKVStore, Transforms, TypeChoices

class LibraryCollectionForm(forms.ModelForm):
    class Meta:
        model = LibraryCollection
        fields = [ 'collection_name', 'description']
        

class TransformsForm(forms.ModelForm):
    class Meta:
        model = Transforms
        fields = "__all__"
        # widgets = {
        #     "value": forms.TextInput(),
        #     "key": forms.TextInput(),
        # }

class TransformKVForm(forms.ModelForm):
    class Meta:
        model = TransformKVStore
        fields = ['key', 'value', 'type']
        widgets = {
            "value": forms.TextInput(),
            "key": forms.TextInput(),
        }

TransformKVFormSet = forms.inlineformset_factory(
    Transforms, TransformKVStore, form=TransformKVForm, extra=1
)