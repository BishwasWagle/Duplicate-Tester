from django import forms
from .models import *

class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['name','file']
        # widgets = {
        #     'server_name': forms.TextInput(),
        #     'server_domain': forms.TextInput(),
        #     'username': forms.TextInput(),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class UpdateThresholdForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['threshold']
        widgets = {
            'threshold': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }