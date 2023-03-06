from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.views import generic, View
from .models import Post, Project


class ProjectList(generic.ListView):
    model = Project
    queryset = Project.objects.filter(status=1).order_by('-created_on')
    template_name = 'projects.html'
    paginate_by = 4


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'posts.html'
    paginate_by = 4


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        # comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_details.html",
            {
                "post": post,
                # "comments": comments,
                "liked": liked
            },
        )


class ProjectDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Project.objects.filter(status=1)
        project = get_object_or_404(queryset, slug=slug)
        # comments = Project.comments.filter(
        #       approved=True).order_by("-created_on")
        liked = False
        if project.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "project_details.html",
            {
                "project": project,
                # "comments": comments,
                "liked": liked
            },
        )
