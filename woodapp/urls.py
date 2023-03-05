from . import views
from django.urls import path

urlpatterns = [
    path("", views.ProjectList.as_view(), name="home"),
    path('posts/', views.PostList.as_view(), name='posts'),
    path('projects/', views.ProjectList.as_view(), name='projects'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_details'),
    path('<slug:slug>/',
         views.ProjectDetail.as_view(), name='project_details'),
]
