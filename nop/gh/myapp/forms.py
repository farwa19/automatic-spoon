from django import forms

class DocumentUploadForm(forms.Form):
    file = forms.FileField(label='Select a PDF or DOCX file')
