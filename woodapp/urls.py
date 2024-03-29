from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('posts/', views.PostList.as_view(), name='posts'),
    path('projects/', views.ProjectList.as_view(), name='projects'),
    # https://stackoverflow.com/questions/63551874/multiple-slugslug-urlpatterns-on-the-root
    path('projects/<slug:slug>',
         views.ProjectDetail.as_view(), name='project_detail'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.ProjectLike.as_view(), name='project_like'),
    path('post_create', views.PostCreate.as_view(), name='post_create'),
    path('project_create', views.ProjectCreate.as_view(),
         name='project_create'),
    path('posts/<slug:slug>/update/', views.PostUpdate.as_view(),
         name='post_update'),
    path('projects/<slug:slug>/update/', views.ProjectUpdate.as_view(),
         name='project_update'),
    path('posts/<slug:slug>/delete/', views.PostDelete.as_view(),
         name='confirm_post_delete'),
    path('projects/<slug:slug>/delete/', views.ProjectDelete.as_view(),
         name='confirm_project_delete'),
]
