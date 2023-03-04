from . import views
from django.urls import path

urlpatterns = [
    path("", views.ProjectList.as_view(), name="home"),
    path('posts/', views.PostList.as_view(), name='posts'),
]
