from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Album

def album_list(request):
    albums_list = Album.objects.filter(is_active=True).order_by('-created_at')
    
    paginator = Paginator(albums_list, 12)
    page_number = request.GET.get('page')
    albums = paginator.get_page(page_number)
    
    context = {
        'albums': albums,
    }
    return render(request, 'gallery/album_list.html', context)

def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk, is_active=True)
    photos = album.photos.all()
    
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'gallery/album_detail.html', context)