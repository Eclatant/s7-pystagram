from django import forms
from django.forms import ValidationError

from .models import Post


class PostSimpleForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'tags']

    def clean_content(self):
        content = self.cleaned_data['content']
        if '바보' in content:
            _msg = '본문에 금지어가 있습니다: {}'.format('바보')
            raise ValidationError(_msg)

        return content  # 주의! 반드시 정제된 결과를 return 함.





