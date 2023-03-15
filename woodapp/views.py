from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Project, Category
from .forms import CommentForm


class ProjectList(ListView):
    model = Project
    queryset = Project.objects.filter(status=1).order_by('-created_on')
    template_name = 'projects.html'
    paginate_by = 4


class PostList(ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'posts.html'
    paginate_by = 4


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
    def post_create(request):
        if request.method == "POST":         
            post_form = AddPostForm(request.POST)
            if post_form.is_valid():              
                post_form.save()              
                messages.success(request, 'Your post was successfully created!')         
                return redirect('seed:view_seed')     

            else:      
                messages.error(request, 'Please correct the error below.')      
        else:
            post_form = PostForm(request.POST)    

        return render(request, "post_create.html")
