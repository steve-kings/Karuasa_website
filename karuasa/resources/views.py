from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Resource, ResourceCategory

def resource_list(request):
    resources_list = Resource.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by resource type
    resource_type = request.GET.get('type', '')
    category_id = request.GET.get('category', '')
    
    if resource_type:
        resources_list = resources_list.filter(resource_type=resource_type)
    
    if category_id:
        resources_list = resources_list.filter(category_id=category_id)
    
    paginator = Paginator(resources_list, 12)
    page_number = request.GET.get('page')
    resources = paginator.get_page(page_number)
    
    categories = ResourceCategory.objects.all()
    
    context = {
        'resources': resources,
        'categories': categories,
        'resource_type': resource_type,
        'category_id': category_id,
    }
    return render(request, 'resources/resource_list.html', context)

def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk, is_active=True)
    related_resources = Resource.objects.filter(
        is_active=True, 
        category=resource.category
    ).exclude(pk=pk)[:4]
    
    context = {
        'resource': resource,
        'related_resources': related_resources,
    }
    return render(request, 'resources/resource_detail.html', context)