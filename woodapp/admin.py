from django.contrib import admin
from .models import Post, Project, Category, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Project)
class ProjectAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'category', 'created_on')
    search_fields = ['title', 'content', 'category']
    list_filter = ('category', 'status')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'category', 'created_on')
    search_fields = ['title', 'content', 'category']
    list_filter = ('category', 'status')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'project', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
