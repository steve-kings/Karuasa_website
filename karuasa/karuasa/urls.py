from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('core.urls')),
    path('members/', include('members.urls')),
    path('events/', include('events.urls')),
    path('projects/', include('projects.urls')),
    path('resources/', include('resources.urls')),
    path('blog/', include('blog.urls')),
    path('gallery/', include('gallery.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)