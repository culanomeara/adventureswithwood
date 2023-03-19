from .models import Comment, Post, Project
from django import forms


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


class ProjectForm(forms.ModelForm):
    """
    Add new project
    """
    class Meta:
        model = Project
        fields = ('title', 'category', 'summary_text', 'featured_image',
                  'tools', 'materials', 'instructions')


    # class UpdatePostForm(forms.ModelForm):
    #     """
    #     Update post
    #     """
    #     class Meta:
    #         model = Post
    #         fields = ('title', 'category', 'excerpt',
    #                 'featured_image', 'content')


    # class UpdateProjectForm(forms.ModelForm):
    #     """
    #     Update project
    #     """
    #     class Meta:
    #         model = Project
    #         fields = ('title', 'category', 'summary_text', 'featured_image',
    #                 'tools', 'materials', 'instructions')
    # """