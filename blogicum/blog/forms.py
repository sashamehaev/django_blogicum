from django import forms
from django.contrib.auth import get_user_model

from .models import Post

User = get_user_model()


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email'
        )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
            'pub_date',
            'author',
        )
