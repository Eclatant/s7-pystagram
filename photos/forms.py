from django import forms


class PostSimpleForm(forms.Form):
    content = forms.CharField()


