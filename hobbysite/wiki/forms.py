from django import forms
from .models import Comment, Article

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment()
        fields = ['entry']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'header_image', 'entry']