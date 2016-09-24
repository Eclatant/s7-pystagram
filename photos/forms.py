from django import forms

from .models import Post


class PostSimpleForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'tags']

