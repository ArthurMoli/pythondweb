from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Course, Review
from .forms import ReviewForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Adicione essa função ao arquivo views.py existente
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now sign in.')
            
            # Automatically log in the user after registration
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            return redirect('course_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form, 'page_title': 'Sign Up'})

def course_list(request):
    courses = Course.objects.annotate(
        avg_rating=Avg('review__rating'),
        num_reviews=Count('review')
    ).order_by('code')
    
    context = {
        'courses': courses,
        'page_title': 'Available Courses'
    }
    return render(request, 'course_list.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reviews = course.review_set.all()
    
    # Check if user has already submitted a review
    user_review = None
    can_review = False
    
    if request.user.is_authenticated:
        user_review = reviews.filter(student=request.user).first()
        can_review = user_review is None
    
    context = {
        'course': course,
        'reviews': reviews,
        'user_review': user_review,
        'can_review': can_review,
        'page_title': course.title
    }
    return render(request, 'course_detail.html', context)

@login_required
def submit_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user already reviewed this course
    if Review.objects.filter(course=course, student=request.user).exists():
        messages.warning(request, 'You have already reviewed this course.')
        return redirect('course_detail', course_id=course.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.student = request.user
            review.course = course
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'course': course,
        'page_title': f'Review {course.title}'
    }
    return render(request, 'submit_review.html', context)

@login_required
def edit_review(request, course_id):
    review = get_object_or_404(Review, course_id=course_id, student=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('course_detail', course_id=course_id)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'course': review.course,
        'page_title': f'Edit Review for {review.course.title}'
    }
    return render(request, 'edit_review.html', context)

@login_required
def delete_review(request, course_id):
    review = get_object_or_404(Review, course_id=course_id, student=request.user)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('course_detail', course_id=course_id)
    
    context = {
        'review': review,   
        'course': review.course,
        'page_title': 'Confirm Deletion'
    }
    return render(request, 'delete_confirm.html', context)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now sign in.')
            
            # Automatically log in the user after registration
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            return redirect('course_list')
    else:
        form = UserCreationForm()
    # Change this line from 'register.html' to the specific path
    return render(request, 'registration/register.html', {'form': form, 'page_title': 'Sign Up'})
