from .models import Comment, Post, Project
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    """
    Add new Comment
    """
    class Meta:
        model = Comment
        fields = ('content',)


class PostForm(forms.ModelForm):
    """
    Add/Update posts
    """
    class Meta:
        model = Post
        fields = ('title', 'category', 'excerpt',
                  'featured_image', 'content')
        widgets = {
            'content': SummernoteWidget(),
        }


class ProjectForm(forms.ModelForm):
    """
    Add/Update project
    """
    class Meta:
        model = Project
        fields = ('title', 'category', 'summary_text', 'featured_image',
                  'tools', 'materials', 'instructions')
        widgets = {
            'tools': SummernoteWidget(),
            'materials': SummernoteWidget(),
            'instructions': SummernoteWidget(),
        }
