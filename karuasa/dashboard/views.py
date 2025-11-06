from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProgress, Course, Competition, CompetitionSubmission
from .forms import ProfileUpdateForm
from django.utils import timezone
import os
import google.generativeai as genai

@login_required
def dashboard(request):
    user_progress, created = UserProgress.objects.get_or_create(member=request.user)
    enrolled_courses = user_progress.completed_courses.count()
    competitions = Competition.objects.filter(is_active=True)
    
    context = {
        'user_progress': user_progress,
        'enrolled_courses': enrolled_courses,
        'competitions': competitions[:3],
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def my_courses(request):
    user_progress, created = UserProgress.objects.get_or_create(member=request.user)
    courses = Course.objects.filter(is_active=True)
    
    context = {
        'courses': courses,
        'user_progress': user_progress,
    }
    return render(request, 'dashboard/my_courses.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    user_progress, created = UserProgress.objects.get_or_create(member=request.user)
    
    context = {
        'course': course,
        'is_completed': course in user_progress.completed_courses.all(),
    }
    return render(request, 'dashboard/course_detail.html', context)

@login_required
def mark_course_complete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user_progress, created = UserProgress.objects.get_or_create(member=request.user)
    
    if course not in user_progress.completed_courses.all():
        user_progress.completed_courses.add(course)
        user_progress.total_points += 100
        user_progress.save()
        messages.success(request, f'Course "{course.name}" marked as complete!')
    
    return redirect('dashboard:my_courses')

@login_required
def competitions(request):
    competitions_list = Competition.objects.filter(is_active=True).order_by('-start_date')
    user_submissions = CompetitionSubmission.objects.filter(participant=request.user)
    
    user_submissions_dict = {sub.competition.id: sub for sub in user_submissions}
    
    context = {
        'competitions': competitions_list,
        'user_submissions': user_submissions,
        'user_submissions_dict': user_submissions_dict,
    }
    return render(request, 'dashboard/competitions.html', context)

@login_required
def competition_detail(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    user_submission = CompetitionSubmission.objects.filter(
        competition=competition, 
        participant=request.user
    ).first()
    
    leaderboard = CompetitionSubmission.objects.filter(
        competition=competition
    ).exclude(score=None).order_by('-score')[:10]
    
    context = {
        'competition': competition,
        'user_submission': user_submission,
        'leaderboard': leaderboard,
    }
    return render(request, 'dashboard/competition_detail.html', context)

@login_required
def submit_competition(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    
    if request.method == 'POST':
        solution = request.POST.get('solution')
        
        if not solution:
            messages.error(request, 'Please provide your solution.')
            return redirect('dashboard:competition_detail', competition_id=competition_id)
        
        existing_submission = CompetitionSubmission.objects.filter(
            competition=competition,
            participant=request.user
        ).first()
        
        if existing_submission:
            messages.error(request, 'You have already submitted a solution for this competition.')
            return redirect('dashboard:competition_detail', competition_id=competition_id)
        
        submission = CompetitionSubmission.objects.create(
            competition=competition,
            participant=request.user,
            solution=solution
        )
        
        score = evaluate_submission_with_ai(competition.problem_statement, solution)
        submission.score = score
        submission.save()
        
        user_progress, created = UserProgress.objects.get_or_create(member=request.user)
        user_progress.total_points += score
        user_progress.save()
        
        messages.success(request, f'Your solution has been submitted! Score: {score}/100')
        return redirect('dashboard:competition_detail', competition_id=competition_id)
    
    return redirect('dashboard:competitions')

@login_required
def progress(request):
    user_progress, created = UserProgress.objects.get_or_create(member=request.user)
    completed_courses = user_progress.completed_courses.all()
    submissions = CompetitionSubmission.objects.filter(participant=request.user)
    
    context = {
        'user_progress': user_progress,
        'completed_courses': completed_courses,
        'submissions': submissions,
    }
    return render(request, 'dashboard/progress.html', context)

@login_required
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard:profile_settings')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'dashboard/profile_settings.html', {'form': form})

def evaluate_submission_with_ai(problem_statement, solution):
    gemini_api_key = os.getenv('GEMINI_API_KEY', '')
    if not gemini_api_key:
        return 75  # Default score if AI is not configured
    
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        As an actuarial science professor, evaluate this student's solution to the following problem:
        
        PROBLEM:
        {problem_statement}
        
        STUDENT'S SOLUTION:
        {solution}
        
        Please evaluate the solution on a scale of 0-100 based on:
        1. Mathematical accuracy (40%)
        2. Logical reasoning (30%)
        3. Completeness (20%)
        4. Clarity and presentation (10%)
        
        Return only the numerical score without any explanation.
        """
        
        response = model.generate_content(prompt)
        score = int(response.text.strip())
        return max(0, min(100, score))  # Ensure score is between 0-100
        
    except Exception as e:
        print(f"AI evaluation error: {e}")
        return 75  # Default score on error