from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.db.models import Sum
from points.models import PointTransaction
from datetime import datetime, timedelta

@login_required
def leaderboard(request):
    # Get top users by total points
    top_users = Profile.objects.filter(is_teacher=False).order_by('-points')[:10]
    
    # Get top users this week
    week_ago = datetime.now() - timedelta(days=7)
    weekly_points = PointTransaction.objects.filter(
        created_at__gte=week_ago
    ).values('user').annotate(
        weekly_total=Sum('points')
    ).order_by('-weekly_total')[:10]
    
    # Get user IDs and create user lookup
    weekly_user_ids = [item['user'] for item in weekly_points]
    weekly_users = Profile.objects.filter(user_id__in=weekly_user_ids, is_teacher=False)
    
    # Combine weekly points with user profiles
    weekly_leaderboard = []
    for points_data in weekly_points:
        try:
            profile = weekly_users.get(user_id=points_data['user'])
            weekly_leaderboard.append({
                'profile': profile,
                'weekly_points': points_data['weekly_total']
            })
        except Profile.DoesNotExist:
            pass
    
    context = {
        'top_users': top_users,
        'weekly_leaderboard': weekly_leaderboard,
    }
    return render(request, 'leaderboard/leaderboard.html', context)