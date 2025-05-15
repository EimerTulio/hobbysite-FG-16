from django import forms
from .models import Comment, Article, ArticleImage


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'header_image', 'entry']


class ArticleDetailForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'header_image', 'entry']


class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        exclude = ['article']
