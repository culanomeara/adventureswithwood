from .models import Comment, Post, Category
from django import forms


class CommentForm(forms.ModelForm):
    """
    Add new Comment
    """
    class Meta:
        model = Comment
        fields = ('content',)


class AddPostForm(forms.ModelForm):
    """
    Add new posts
    """
    class Meta:
        model = Post
        fields = ('title', 'author', 'category', 'excerpt',
                  'featured_image', 'content')
