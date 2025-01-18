from django import forms
from .models import Document

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'hidden': True, 'id': 'fileInput'}))


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file']  # Adjust fields as needed