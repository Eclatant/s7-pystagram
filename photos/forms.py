from django import forms
from django.forms import ValidationError

from .models import Post

class PostSimpleForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, help_text=
    '글 본문은 재밋게')
    #tag = forms.CharField(required=False)

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'image', 'tags']

    def clean_content(self):
        content = self.cleaned_data['content']
        if '바보' in content:
            _msg = '본문에 금지어가 있습니다 : {}'.format('바보')
            raise ValidationError(_msg)

        return content # 주의! 반드시 정제된 결과를 return 함.

    def clean(self):
        content = self.cleaned_data.get('content')
        if content and '띨띨이' in content:
            _msg = '방심하지마라 금지어 있다 : {}'.format('띨띨이')
            self.add_error('content', _msg)
