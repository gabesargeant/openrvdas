from django import forms
from .models import LibraryCollection, ConfigObjectStore
from django.core.exceptions import ValidationError

class LibraryCollectionForm(forms.ModelForm):
    class Meta:
        model = LibraryCollection
        fields = ["collection_name", "description"]


class ConfigObjectStoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fields read-only
        self.fields["name"].widget.attrs["readonly"] = True
        self.fields["class_name"].widget.attrs["readonly"] = True
        self.fields["json_object"].widget.attrs["readonly"] = True

    class Meta:
        model = ConfigObjectStore
        fields = ["name", "description", "class_name", "json_object"]



class BaseRVDASConfigForm(forms.Form):
    name = forms.CharField(required=False)
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    description = forms.CharField(widget=forms.Textarea, label="Description")


class LoggerForm(BaseRVDASConfigForm):
    pass
    