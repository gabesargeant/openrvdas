from django import forms
from .models import  ConfigObjectStore
from django.core.exceptions import ValidationError
from django.db.models import Case, When, IntegerField



class ConfigObjectStoreForm(forms.ModelForm):
    class Meta:
        model = ConfigObjectStore
        fields = [ "id", "name", "description", "class_name", "json_object"]
        widgets = {            
             'id': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fields read-only
        self.fields["name"].widget.attrs["readonly"] = True
        self.fields["class_name"].widget.attrs["readonly"] = True
        self.fields["json_object"].widget.attrs["readonly"] = True
        print(self.fields)
        print("testtesttetste")
        

    
    

class BaseRVDASConfigForm(forms.Form):
    name = forms.CharField(required=False)
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    description = forms.CharField(widget=forms.Textarea, label="Description")


READER_CHOICES = []
TRANSFORM_CHOICES = []
WRITER_CHOICES = []
STDERR_WRITER_CHOICES = []



class ListenerForm(BaseRVDASConfigForm):
    def __init__(self, *args, **kwargs):
        # Extract custom arguments
        
        name = kwargs.pop('name', None)
        description = kwargs.pop('description', None)

        # objects
        readers = kwargs.pop('readers', None)
        transforms = kwargs.pop('transforms', None)
        writers = kwargs.pop('writers', None)
        stderr_writers = kwargs.pop('stderr_writers', None)

        # logger configs
        host_id = kwargs.pop('host_id', None)
        interval = kwargs.pop('interval', None)
        check_format = kwargs.pop('check_format', None)
        
        id = kwargs.pop('id', None)

        super(ListenerForm, self).__init__(*args, **kwargs)

        if id:
            self.fields['id'].initial = id

        if name:
            self.fields['name'].initial = name
        if description:
            self.fields['description'].initial = description

        # config
        if readers:
            preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(readers)], output_field=IntegerField())
            reader_objects = ConfigObjectStore.objects.filter(id__in=readers).order_by(preserved_order)
            self.fields['readers'].choices = [(obj.id, f"{obj.id} : {obj.name}") for obj in reader_objects]
            self.fields['readers'].initial = [obj.id for obj in reader_objects]
        else:
            self.fields['readers'].choices = []
        if transforms:
            preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(transforms)], output_field=IntegerField())
            transform_objects = ConfigObjectStore.objects.filter(id__in=transforms).order_by(preserved_order)
            self.fields['transforms'].choices = [(obj.id, f"{obj.id} : {obj.name}") for obj in transform_objects]
            self.fields['transforms'].initial = [obj.id for obj in transform_objects]
        else:
            self.fields['transforms'].choices = []

        if writers:
            preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(writers)], output_field=IntegerField())
            writer_objects = ConfigObjectStore.objects.filter(id__in=writers).order_by(preserved_order)
            self.fields['writers'].choices = [(obj.id, f"{obj.id} : {obj.name}") for obj in writer_objects]
            self.fields['writers'].initial = [obj.id for obj in writer_objects]
        else:
            self.fields['writers'].choices = []

        if stderr_writers:
            preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(stderr_writers)], output_field=IntegerField())
            stderr_writers_objects = ConfigObjectStore.objects.filter(id__in=stderr_writers).order_by(preserved_order)
            self.fields['stderr_writers'].choices = [(obj.id, f"{obj.id} : {obj.name}") for obj in stderr_writers_objects]
            self.fields['stderr_writers'].initial = [obj.id for obj in stderr_writers_objects]
        else:
            self.fields['stderr_writers'].choices = []

        # logger stuff

        if host_id:
            self.fields['host_id'].initial = host_id
        if interval:
            self.fields['interval'].initial = interval
        if check_format:
            self.fields['check_format'].initial = check_format

    readers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False, help_text="Selected readers.")
    transforms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False, help_text="Selected transforms.")
    writers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False, help_text="Selected writers.")
    stderr_writers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False, help_text="Selected stderr writers.")
    host_id = forms.CharField(max_length=255, required=False, help_text="Enter the host ID.", initial='')
    interval = forms.IntegerField(min_value=0, required=False, help_text="Enter the interval in seconds.", initial=0)
    check_format = forms.BooleanField(required=False, initial=False, help_text="Check this box to check the format.")


class ComposedReaderForm(BaseRVDASConfigForm):
    def __init__(self, *args, **kwargs):
        # Extract custom arguments
        name = kwargs.pop('name', None)
        description = kwargs.pop('description', None)

        # objects
        readers = kwargs.pop('readers', None)
        transforms = kwargs.pop('transforms', None)                
        check_format = kwargs.pop('check_format', False)
        

        super(ComposedReaderForm, self).__init__(*args, **kwargs)

        if name:
            self.fields['name'].initial = name
        if description:
            self.fields['description'].initial = description

        # config
        if readers:
            preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(readers)], output_field=IntegerField())
            reader_objects = ConfigObjectStore.objects.filter(id__in=readers).order_by(preserved_order)
            self.fields['readers'].choices = [(obj.id, f"{obj.id} : {obj.name}") for obj in reader_objects]
            self.fields['readers'].initial = [obj.id for obj in reader_objects]
        else:
            self.fields['readers'].choices = []
        if transforms:
            preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(transforms)], output_field=IntegerField())
            transform_objects = ConfigObjectStore.objects.filter(id__in=transforms).order_by(preserved_order)
            self.fields['transforms'].choices = [(obj.id, f"{obj.id} : {obj.name}") for obj in transform_objects]
            self.fields['transforms'].initial = [obj.id for obj in transform_objects]
        else:
            self.fields['transforms'].choices = []

        if check_format:
            self.fields['check_format'].initial = check_format

    readers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False, help_text="Selected readers.")
    transforms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False, help_text="Selected transforms.")   
    check_format = forms.BooleanField(required=False, help_text="Check this box to check the format.")