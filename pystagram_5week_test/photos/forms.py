from django import forms
from django.core.exceptions import ValidationError

from .models import Photo, Comment

class PostSimpleForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class PhotoForm(forms.ModelForm):
    tags = forms.CharField(required=False)
    class Meta:
        model = Photo
        fields = ['title', 'content', 'tags']

    def clean_content(self):
        content = self.cleaned_data['content']
        if '바보' in content :
            _msg = '본문에 금지어가 있습니다 : {}'.format('바보')
            raise ValidationError(_msg) # Exception 에러이므로 발생하면 중단함

        return content # 주의! 반드시 정제된 결과를 return 함.
    def clean(self):
        content = self.cleaned_data.get('content')
        if content and '띨띨이' in content:
            _msg = '방심하지 마라! 금지어 있다 : {}'.format('띨띨이')
            self.add_error('content', _msg)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data['content']
        if '바보' in content :
            _msg = '본문에 금지어가 있습니다 : {}'.format('바보')
            raise ValidationError(_msg) # Exception 에러이므로 발생하면 중단함

        return content # 주의! 반드시 정제된 결과를 return 함.
    def clean(self):
        content = self.cleaned_data.get('content')
        if content and '띨띨이' in content:
            _msg = '방심하지 마라! 금지어 있다 : {}'.format('띨띨이')
            self.add_error('content', _msg)

class PhotoDeleteForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = []

class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = []

