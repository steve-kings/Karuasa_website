# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.my_courses, name='my_courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/complete/', views.mark_course_complete, name='mark_course_complete'),
    path('competitions/', views.competitions, name='competitions'),
    path('competitions/<int:competition_id>/', views.competition_detail, name='competition_detail'),
    path('competitions/<int:competition_id>/submit/', views.submit_competition, name='submit_competition'),
    path('progress/', views.progress, name='progress'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
]