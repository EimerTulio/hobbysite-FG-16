from django import forms
from .models import Thread, Comment
"""
Thread Create View
All fields should be available. The Created On and Updated On is automatically set, and the Author is the logged in user. These three fields should not be editable.
Category field should be a dropdown.
This should only be accessible to logged-in users.
Thread Update View
It should allow updates of all fields except for the Created On and Author field.
This should only be accessible to logged-in users.
"""

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "category", "entry", "image"]

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields=[]