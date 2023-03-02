from django.shortcuts import render
from django.views import generic
from .models import Post, Project


class ProjectList(generic.ListView):
    model = Project
    queryset = Project.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 4
