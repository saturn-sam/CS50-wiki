from django import forms

class SearchForm(forms.Form):
    page = forms.CharField(widget=forms.TextInput(attrs={'class' : 'charfield1', 'placeholder': 'Wiki Search'}),label='')

class CreateWikiForm(forms.Form):
    title = forms.CharField(label= "Title")
    content = forms.CharField(widget=forms.Textarea(), label='')

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='')