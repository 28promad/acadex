from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from points.models import PointTransaction

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    recent_points = PointTransaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'recent_points': recent_points,
    }
    return render(request, 'core/dashboard.html', context)