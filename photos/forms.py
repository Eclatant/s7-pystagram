from django import forms

from .models import Post


class PostSimpleForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'tags']

