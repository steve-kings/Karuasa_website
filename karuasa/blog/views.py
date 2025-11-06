from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import BlogPost, BlogComment
from .forms import BlogPostForm, BlogCommentForm
from django.views.decorators.http import require_POST
from .models import BlogPost

def post_list(request):
    posts_list = BlogPost.objects.filter(
        is_published=True, 
        is_approved=True
    ).order_by('-created_at')
    
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_published=True, is_approved=True)
    comments = post.comments.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to comment.')
            return redirect('members:login')
        
        comment_form = BlogCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('blog:post_detail', pk=pk)
    else:
        comment_form = BlogCommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_approved = False  # Wait for admin approval
            post.save()
            messages.success(request, 'Your post has been submitted for approval!')
            return redirect('blog:post_list')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/add_post.html', {'form': form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.likes += 1
    post.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'likes': post.likes})
    
    messages.success(request, 'Post liked!')
    return redirect('blog:post_detail', pk=pk)


@require_POST
def share_post(request, post_id):
    try:
        post = BlogPost.objects.get(id=post_id)
        post.shares += 1
        post.save()
        return JsonResponse({
            'success': True,
            'new_share_count': post.shares
        })
    except BlogPost.DoesNotExist:
        return JsonResponse({'success': False}, status=404)