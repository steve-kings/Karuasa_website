from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('add/', views.add_project, name='add_project'),
    path('projects/<int:pk>/like/', views.like_project, name='like_project'),
    path('projects/<int:pk>/share/', views.share_project, name='share_project'),
]