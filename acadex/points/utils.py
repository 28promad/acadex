from .models import PointTransaction
from accounts.models import Profile
from datetime import date, timedelta

def award_points(user, points, point_type, description):
    """Award points to a user and update their profile"""
    if points <= 0:
        return
    
    # Create transaction
    PointTransaction.objects.create(
        user=user,
        points=points,
        point_type=point_type,
        description=description
    )
    
    # Update user's total points
    profile, created = Profile.objects.get_or_create(user=user)
    profile.points += points
    profile.last_activity = date.today()
    
    # Update streak
    if profile.last_activity:
        if profile.last_activity == date.today() - timedelta(days=1):
            profile.streak_days += 1
        elif profile.last_activity != date.today():
            profile.streak_days = 1
    else:
        profile.streak_days = 1
    
    profile.save()
    return profile.points

def calculate_improvement_points(user, new_score, subject):
    """Calculate and award points based on improvement"""
    from records.models import TestRecord
    
    # Get last score in this subject
    previous_records = TestRecord.objects.filter(
        student=user, 
        subject=subject
    ).exclude(score=new_score).order_by('-test_date')
    
    if previous_records.exists():
        last_record = previous_records.first()
        last_percentage = (last_record.score / last_record.max_score) * 100
        improvement = new_score - last_percentage
        
        if improvement > 0:
            points = max(int(improvement * 2), 1)  # At least 1 point for any improvement
            award_points(user, points, 'improvement', f'Improved by {improvement:.1f}% in {subject}')
            return points
    
    return 0