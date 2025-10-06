from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']

    def __init__(self, *args, include_categories=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not include_categories:
            self.fields.pop('categories')
