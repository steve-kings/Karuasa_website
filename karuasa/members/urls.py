from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.members_list, name='members_list'),
    path('register/', views.register, name='register'),
    path('login/', views.member_login, name='login'),
    path('logout/', views.member_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]