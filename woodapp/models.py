from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# base code from CI video lesson:
# https://github.com/Code-Institute-Solutions/Django3blog/blob/master/04_building_the_models/blog/models.py

STATUS = ((0, "Draft"), (1, "Published"))


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects"
    )
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name="proj_categories")
    featured_image = CloudinaryField('image', default='')
    tools = models.TextField()
    materials = models.TextField()
    instructions = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='project_like', blank=True)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name="post_categories")
    excerpt = models.TextField(blank=True)
    featured_image = CloudinaryField('image', default='')
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='post_like', blank=True)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="comments")
    name = models.CharField(max_length=80)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.content} by {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
