from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))
APPROVED = ((0, "Awaiting Approval"), (1, "Approved"))


class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects"
    )
    category = models.ForeignKey(Category, related_name="categories")
    featured_image = CloudinaryField('image', default='placeholder')
    tools = models.TextField()
    materials = models.TextField()
    instructions = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='project_like', blank=True)
    approved = models.IntegerField(choices=APPROVED, default=0)
