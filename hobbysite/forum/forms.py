from django import forms

from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "category", "entry", "image"]


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']
