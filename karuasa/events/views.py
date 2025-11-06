from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Event

def event_list(request):
    events_list = Event.objects.filter(is_active=True).order_by('-date')
    
    # Filter by event type
    event_type = request.GET.get('type', '')
    if event_type:
        events_list = events_list.filter(event_type=event_type)
    
    paginator = Paginator(events_list, 9)
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    
    context = {
        'events': events,
        'event_type': event_type,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_active=True)
    related_events = Event.objects.filter(
        is_active=True, 
        event_type=event.event_type
    ).exclude(pk=pk)[:3]
    
    context = {
        'event': event,
        'related_events': related_events,
    }
    return render(request, 'events/event_detail.html', context)