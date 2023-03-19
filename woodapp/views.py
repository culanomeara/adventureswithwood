from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.utils.text import slugify
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView, UpdateView
from .models import Post, Project, Category
from .forms import CommentForm, AddPostForm, AddProjectForm, UpdatePostForm, UpdateProjectForm


class ProjectList(ListView):
    model = Project
    queryset = Project.objects.filter(status=1).order_by('-created_on')
    template_name = 'projects.html'


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'posts.html'


class PostDetail(DetailView):

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


class ProjectDetail(DetailView):

    def get(self, request, slug, *args, **kwargs):
        queryset = Project.objects.filter(status=1)
        project = get_object_or_404(queryset, slug=slug)
        comments = project.comments.filter(
               approved=True).order_by("-created_on")
        liked = False
        if project.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "project_details.html",
            {
                "project": project,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Project.objects.filter(status=1)
        project = get_object_or_404(queryset, slug=slug)
        comments = project.comments.filter(
               approved=True).order_by("-created_on")
        liked = False
        if project.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.project = project
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "project_details.html",
            {
                "project": project,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class ProjectLike(ListView):
    def post(self, request, slug, *args, **kwargs):
        project = get_object_or_404(Project, slug=slug)
        if project.likes.filter(id=self.request.user.id).exists():
            project.likes.remove(request.user)
        else:
            project.likes.add(request.user)
        return HttpResponseRedirect(reverse('project_detail', args=[slug]))


# https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.mixins.LoginRequiredMixin
# https://stackoverflow.com/questions/66438829/how-can-i-connect-the-user-to-a-post-he-created-in-django
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'category', 'excerpt', 'featured_image', 'content')
    template_name = "post_create.html"

    def post(self, request, *args, **kwargs):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(request,
                             'You have submitted '
                             'your post: <strong>%s</strong> for approval!'
                             % post.title)
        else:
            form = AddPostForm()
        return redirect('posts')


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ('title', 'category', 'summary_text', 'featured_image', 'tools',
              'materials', 'instructions')
    template_name = "project_create.html"

    def post(self, request, *args, **kwargs):
        form = AddProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.slug = slugify(project.title)
            project.save()
            messages.success(request,
                             'You have submitted '
                             'your project: <strong>%s</strong> for approval!'
                             % project.title)
        else:
            form = AddProjectForm()
        return redirect('projects')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'category', 'excerpt', 'featured_image', 'content')
    template_name = "post_update.html"

    def post(self, request, *args, **kwargs):
        form = UpdatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request,
                             'You have updated '
                             'your post: <strong>%s</strong>'
                             % post.title)
        else:
            form = UpdatePostForm()
        return redirect('posts')


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ('title', 'category', 'summary_text', 'featured_image', 'tools',
              'materials', 'instructions')
    template_name = "project_update.html"

    def post(self, request, *args, **kwargs):
        form = UpdateProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.slug = slugify(project.title)
            project.save()
            messages.success(request,
                             'You have updated '
                             'your project: <strong>%s</strong>'
                             % project.title)
        else:
            form = UpdateProjectForm()
        return redirect('projects')
