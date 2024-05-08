from django import forms
from .models import LibraryCollection, TransformKVStore, Transforms, TypeChoices

class CachedDataReaderForm(forms.Form):
    object_class = forms.CharField(label='class', initial='CachedDataReader', disabled=True)
    data_server = forms.CharField(label='data_server', initial='localhost:8766')
    use_wss = forms.BooleanField(label='use_wss', initial=False, required=False)
    check_cert=forms.BooleanField(label='check_cert', initial=False, required=False)  
    # Serializer is a dict formset
    #Subscription_fields

class SubscriptionFields(forms.Form):
    field = forms.CharField(label='field')
    seconds = forms.IntegerField(label='seconds', initial=0)
    pass

