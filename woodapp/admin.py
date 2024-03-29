from django.contrib import admin
from .models import Post, Project, Category, Comment
from django_summernote.admin import SummernoteModelAdmin


class ProjectAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'category', 'created_on')
    search_fields = ['title', 'content', 'category']
    list_filter = ('category', 'status')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('tools', 'materials', 'instructions')


admin.site.register(Project, ProjectAdmin)


class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'category', 'created_on')
    search_fields = ['title', 'content', 'category']
    list_filter = ('category', 'status')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

    def filtered_category(self, obj):
        return Category.objects.filter(type=1)


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'project', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


admin.site.register(Comment, CommentAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name', 'type')


admin.site.register(Category, CategoryAdmin)
