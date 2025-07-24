from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Flashcard, QuizAttempt
from points.utils import award_points
import random

@login_required
def create_flashcard(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        question = request.POST['question']
        answer = request.POST['answer']
        is_public = request.POST.get('is_public', False)
        
        Flashcard.objects.create(
            creator=request.user,
            subject=subject,
            question=question,
            answer=answer,
            is_public=bool(is_public)
        )
        
        # Award points for creating flashcard
        award_points(request.user, 5, 'study', f'Created flashcard in {subject}')
        
        messages.success(request, "Flashcard created! +5 points 🎉")
        return redirect('flashcard_list')
    
    return render(request, 'flashcards/create.html')

@login_required
def flashcard_list(request):
    # Show user's own flashcards and public ones
    flashcards = Flashcard.objects.filter(
        models.Q(creator=request.user) | models.Q(is_public=True)
    ).order_by('-created_at')
    
    return render(request, 'flashcards/list.html', {'flashcards': flashcards})

@login_required
def study_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    
    if request.method == 'POST':
        user_answer = request.POST['user_answer'].strip().lower()
        correct_answer = flashcard.answer.strip().lower()
        is_correct = user_answer == correct_answer
        
        # Record attempt
        QuizAttempt.objects.create(
            user=request.user,
            flashcard=flashcard,
            correct=is_correct
        )
        
        # Award points for correct answer
        if is_correct:
            award_points(request.user, 2, 'quiz', f'Correct answer in {flashcard.subject}')
            messages.success(request, "Correct! +2 points 🎉")
        else:
            messages.error(request, f"Wrong answer. Correct answer was: {flashcard.answer}")
        
        return redirect('flashcard_list')
    
    return render(request, 'flashcards/study.html', {'flashcard': flashcard})
