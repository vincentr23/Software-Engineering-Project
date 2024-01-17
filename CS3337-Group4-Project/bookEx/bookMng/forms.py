from django import forms
from django.forms import ModelForm
from .models import Book, Feedback


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

