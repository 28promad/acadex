from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import TestRecord
from points.utils import award_points, calculate_improvement_points

@login_required
def upload_record(request):
    # Only teachers can upload
    if not request.user.profile.is_teacher:
        messages.error(request, "Only teachers can upload test scores!")
        return redirect('dashboard')
    
    if request.method == 'POST':
        student_username = request.POST['student_username']
        subject = request.POST['subject']
        score = float(request.POST['score'])
        max_score = float(request.POST.get('max_score', 100))
        test_date = request.POST['test_date']
        
        try:
            student = User.objects.get(username=student_username)
        except User.DoesNotExist:
            messages.error(request, f"Student '{student_username}' not found!")
            return render(request, 'records/upload.html')
        
        # Create test record
        TestRecord.objects.create(
            student=student,
            teacher=request.user,
            subject=subject,
            score=score,
            max_score=max_score,
            test_date=test_date
        )
        
        # Award base points for test participation
        percentage = (score / max_score) * 100
        base_points = int(percentage / 10)  # 10 points for 100%, 5 for 50%, etc.
        award_points(student, base_points, 'test', f'Test in {subject}: {score}/{max_score}')
        
        # Award improvement points if applicable
        improvement_points = calculate_improvement_points(student, percentage, subject)
        
        total_points = base_points + improvement_points
        messages.success(request, f"Test uploaded! {student.username} earned {total_points} points.")
        
        return redirect('upload_record')
    
    return render(request, 'records/upload.html')

@login_required
def view_records(request):
    if request.user.profile.is_teacher:
        # Teachers see all records they uploaded
        records = TestRecord.objects.filter(teacher=request.user)
    else:
        # Students see their own records
        records = TestRecord.objects.filter(student=request.user)
    
    context = {'records': records}
    return render(request, 'records/view_records.html', context)
