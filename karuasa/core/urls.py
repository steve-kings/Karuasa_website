from django.urls import path
from .views import constitution_view
from . import views

urlpatterns = [
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('testimonial/', views.submit_testimonial, name='submit_testimonial'),
    path('constitution/', constitution_view, name='constitution'),
    path('admin/messages/', views.admin_message_list, name='admin_message_list'),
    path('admin/messages/<int:message_id>/', views.admin_message_detail, name='admin_message_detail'),
    path('chatbot-api/', views.chatbot_api, name='chatbot_api'),
]