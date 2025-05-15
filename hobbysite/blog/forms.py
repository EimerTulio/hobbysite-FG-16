from django import forms
from .models import Comment, Article


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'header_image']

    def clean_header_image(self):
        image = self.cleaned_data.get('header_image')
        if image and image.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Image too large (max 2MB)")
        return image
