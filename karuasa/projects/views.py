from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Project, ProjectComment
from .forms import ProjectForm, ProjectCommentForm
from django.views.decorators.http import require_POST

def project_list(request):
    projects_list = Project.objects.filter(is_approved=True).order_by('-created_at')
    
    # Filter featured projects
    featured = request.GET.get('featured', '')
    if featured:
        projects_list = projects_list.filter(is_featured=True)
    
    paginator = Paginator(projects_list, 9)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    context = {
        'projects': projects,
        'featured': featured,
    }
    return render(request, 'projects/project_list.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, is_approved=True)
    comments = project.comments.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to comment.')
            return redirect('members:login')
        
        comment_form = ProjectCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.project = project
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('projects:project_detail', pk=pk)
    else:
        comment_form = ProjectCommentForm()
    
    context = {
        'project': project,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.is_approved = False  # Wait for admin approval
            project.save()
            project.members.add(request.user)
            messages.success(request, 'Your project has been submitted for approval!')
            return redirect('projects:project_list')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/add_project.html', {'form': form})


@require_POST
@login_required
def like_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        project.likes += 1
        project.save()
        
        return JsonResponse({
            'success': True,
            'new_like_count': project.likes
        })
    except Project.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

@require_POST
def share_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        project.shares += 1
        project.save()
        return JsonResponse({
            'success': True,
            'new_share_count': project.shares
        })
    except Project.DoesNotExist:
        return JsonResponse({'success': False}, status=404)