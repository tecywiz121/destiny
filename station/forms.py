from django import forms
from django.core import validators

class PuzzleForm(forms.Form):
    solution = forms.CharField()

class CommunicationForm(forms.Form):
    message = forms.CharField()

class AdminForm(forms.Form):
    confirmation = forms.CharField()

    def clean_confirmation(self):
        if self.cleaned_data['confirmation'].lower() != 'confirm':
            raise forms.ValidationError('You must type `confirm` to engage self destruct')
        return self.cleaned_data['confirmation']
