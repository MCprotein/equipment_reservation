from django import forms
from .models import Blog


# 만약 모델 기반이 아니라면 forms.Form
class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['category', 'title', 'description']

        labels = {
            'category': '카테고리',
            'title': '제목',
            'description': '내용',
        }
