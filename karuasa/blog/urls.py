from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('add/', views.add_post, name='add_post'),
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/share/', views.share_post, name='share_post'),
]