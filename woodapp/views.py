from django.shortcuts import (render,
                              get_object_or_404,
                              reverse,
                              redirect)
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (View,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView)
from .models import Post, Project, Category
from .forms import CommentForm, PostForm, ProjectForm


class Home(View):
    """
    A class for the Home page view
    """
    def get(self, request, *args, **kwargs):
        featured_projects = (
            Project.objects.all().order_by('-created_on')[:5]
        )
        most_popular = Project.objects.all().order_by('likes')[:3]
        most_recent = Category.objects.all().order_by('type')[:6]
        posts = Post.objects.all().order_by('-created_on')[:2]

        context = {
            'featured_projects': featured_projects,
            'most_popular': most_popular,
            'most_recent': most_recent,
            'posts': posts
        }
        return render(request, 'index.html', context)


class ProjectList(ListView):
    """
    A class for the ProjectList view
    """
    model = Project
    queryset = Project.objects.filter(status=1).order_by('-created_on')
    template_name = 'projects.html'


class PostList(ListView):
    """
    A class for the PostList view
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'posts.html'


class PostDetail(DetailView):
    """
    A class for the PostDetail view
    """
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
    """
    A class for the ProjectDetail view
    """
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
    """
    A class for the ProjectLike view
    """
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
    """
    A class for the PostCreate view
    """
    model = Post
    fields = ('title', 'category', 'excerpt', 'featured_image', 'content')
    template_name = "post_create.html"

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(request,
                             'You have submitted '
                             'your post: <strong>%s</strong>!'
                             % post.title)
        else:
            form = PostForm()
        return redirect('posts')


class ProjectCreate(LoginRequiredMixin, CreateView):
    """
    A class for the ProjectCreate view
    """
    model = Project
    fields = ('title', 'category', 'summary_text', 'featured_image', 'tools',
              'materials', 'instructions')
    template_name = "project_create.html"

    def post(self, request, *args, **kwargs):
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.slug = slugify(project.title)
            project.save()
            messages.success(request,
                             'You have submitted '
                             'your project: <strong>%s</strong>!'
                             % project.title)
        else:
            form = ProjectForm()
        return redirect('projects')


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A class for the PostUdpate view
    """
    model = Post
    fields = ('title', 'category', 'excerpt', 'featured_image', 'content')
    template_name = "post_update.html"

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.slug = slugify(post.title)
            post = form.save(commit=False)
            post.save()
            messages.success(request,
                             'You have updated '
                             'your post: <strong>%s</strong>'
                             % post.title)
        else:
            messages.warning(request,
                             'You have not updated '
                             'your post')
            # form = UpdatePostForm()
        return redirect('posts')

# https://www.youtube.com/watch?v=-s7e_Fy6NRU

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ProjectUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    A class for the ProjectUpdate view
    """
    model = Project
    fields = ('title', 'category', 'summary_text', 'featured_image', 'tools',
              'materials', 'instructions')
    template_name = "project_update.html"

    def post(self, request, slug, *args, **kwargs):
        project = get_object_or_404(Project, slug=slug)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project.slug = slugify(project.title)
            project = form.save(commit=False)
            project.save()
            messages.success(request,
                             'You have updated '
                             'your project: <strong>%s</strong>'
                             % project.title)
        else:
            messages.warning(request, 'You have not updated '
                             'your project')
        return redirect('projects')

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A class for the PostDelete view
    """
    model = Post
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('posts')
# https://stackoverflow.com/questions/17678689/how-to-add-a-cancel-button-to-deleteview-in-django

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            messages.success(request,
                             'You have successfully deleted your post')
            return super(PostDelete, self).post(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class ProjectDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    A class for the ProjectDelete view
    """
    model = Project
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('projects')
# https://stackoverflow.com/questions/17678689/how-to-add-a-cancel-button-to-deleteview-in-django

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            messages.success(request,
                             'You have successfully deleted your project')
            return super(ProjectDelete, self).post(request, *args, **kwargs)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False
