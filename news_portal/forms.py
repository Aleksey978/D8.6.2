from django import forms
from .models import Post, news, Category


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
       ]

class SubscribeForm(forms.Form):
    category_id = forms.IntegerField(widget=forms.HiddenInput())