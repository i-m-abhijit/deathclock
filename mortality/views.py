from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import models
from .models import (UserProfile, TimeWasteEntry, TimeWasteCategory, MortalityReflection,
                    MortalityPost, MortalityChallenge, ChallengeParticipant, MortalityLeaderboard)
from .forms import UserProfileForm, TimeWasteEntryForm, ReflectionForm
from datetime import date
import json

def home(request):
    """Landing page with stark mortality reminder"""
    context = {
        'show_mortality_facts': True
    }
    return render(request, 'mortality/home.html', context)

@login_required
def dashboard(request):
    """Main dashboard showing user's mortality statistics"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('setup_profile')
    
    # Calculate time waste statistics
    time_wastes = TimeWasteEntry.objects.filter(user=request.user)
    total_daily_waste = sum(entry.hours_per_day for entry in time_wastes)
    
    # Calculate lifetime waste
    lifetime_waste_days = sum(entry.days_wasted_lifetime() for entry in time_wastes)
    
    context = {
        'profile': profile,
        'age': profile.age(),
        'days_lived': profile.days_lived(),
        'days_remaining': profile.estimated_days_remaining(),
        'life_percentage': round(profile.life_percentage_lived(), 1),
        'weeks_remaining': profile.weeks_remaining(),
        'total_daily_waste': total_daily_waste,
        'lifetime_waste_days': round(lifetime_waste_days, 1),
        'time_wastes': time_wastes,
        'recent_reflections': MortalityReflection.objects.filter(user=request.user).order_by('-created_at')[:3]
    }
    return render(request, 'mortality/dashboard.html', context)

@login_required
def setup_profile(request):
    """Setup user's mortality profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your mortality profile has been created. Face your reality.')
            return redirect('dashboard')
    else:
        form = UserProfileForm()
    
    return render(request, 'mortality/setup_profile.html', {'form': form})

@login_required
def time_waste_tracker(request):
    """Track daily time waste"""
    if request.method == 'POST':
        form = TimeWasteEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.warning(request, f'Logged {entry.hours_per_day} hours of daily waste on {entry.category.name}. Time you\'ll never get back.')
            return redirect('time_waste_tracker')
    else:
        form = TimeWasteEntryForm()
    
    entries = TimeWasteEntry.objects.filter(user=request.user).order_by('-date_logged')
    categories = TimeWasteCategory.objects.all()
    
    return render(request, 'mortality/time_waste.html', {
        'form': form,
        'entries': entries,
        'categories': categories
    })

@login_required
def mortality_reflection(request):
    """Record mortality reflections"""
    if request.method == 'POST':
        form = ReflectionForm(request.POST)
        if form.is_valid():
            reflection = form.save(commit=False)
            reflection.user = request.user
            reflection.save()
            messages.info(request, 'Reflection saved. Remember: awareness is the first step to change.')
            return redirect('mortality_reflection')
    else:
        form = ReflectionForm()
    
    reflections = MortalityReflection.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'mortality/reflections.html', {
        'form': form,
        'reflections': reflections
    })



@login_required
def life_visualization(request):
    """Visual representation of life remaining"""
    try:
        profile = request.user.userprofile
        weeks_lived = profile.days_lived() // 7
        weeks_total = int(profile.life_expectancy * 52.18)  # 52.18 weeks per year
        weeks_remaining = weeks_total - weeks_lived
        
        context = {
            'weeks_lived': weeks_lived,
            'weeks_remaining': max(0, weeks_remaining),
            'weeks_total': weeks_total,
            'life_percentage': profile.life_percentage_lived()
        }
        return render(request, 'mortality/life_visualization.html', context)
    except UserProfile.DoesNotExist:
        return redirect('setup_profile')

# MORTALITY SOCIAL NETWORK VIEWS

@login_required
def social_feed(request):
    """Main social feed showing mortality posts"""
    posts = MortalityPost.objects.all().order_by('-created_at')[:20]
    active_challenges = MortalityChallenge.objects.filter(is_active=True)[:5]
    
    # Get user's anonymous username
    profile = request.user.userprofile
    anonymous_username = profile.generate_anonymous_username()
    
    context = {
        'posts': posts,
        'active_challenges': active_challenges,
        'anonymous_username': anonymous_username,
    }
    return render(request, 'mortality/social_feed.html', context)

@login_required
def create_post(request):
    """Create a new mortality post"""
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        MortalityPost.objects.create(
            user=request.user,
            post_type=post_type,
            title=title,
            content=content,
            is_anonymous=is_anonymous
        )
        
        messages.success(request, 'Your mortality post has been shared with the community.')
        return redirect('social_feed')
    
    return render(request, 'mortality/create_post.html')

@login_required
def mortality_challenges(request):
    """View and join mortality challenges"""
    active_challenges = MortalityChallenge.objects.filter(is_active=True)
    user_challenges = ChallengeParticipant.objects.filter(user=request.user)
    
    context = {
        'active_challenges': active_challenges,
        'user_challenges': user_challenges,
    }
    return render(request, 'mortality/challenges.html', context)

@login_required
def join_challenge(request, challenge_id):
    """Join a mortality challenge"""
    challenge = get_object_or_404(MortalityChallenge, id=challenge_id)
    
    participant, created = ChallengeParticipant.objects.get_or_create(
        challenge=challenge,
        user=request.user
    )
    
    if created:
        messages.success(request, f'You joined the challenge: {challenge.title}')
    else:
        messages.info(request, 'You are already participating in this challenge.')
    
    return redirect('mortality_challenges')

@login_required
def mortality_leaderboard(request):
    """Show mortality leaderboards"""
    from django.utils import timezone
    from datetime import timedelta
    
    # Get current week's leaderboard
    week_ending = timezone.now().date()
    
    leaderboards = {
        'least_waste': MortalityLeaderboard.objects.filter(
            leaderboard_type='least_waste',
            week_ending=week_ending
        ).order_by('rank')[:10],
        'most_productive': MortalityLeaderboard.objects.filter(
            leaderboard_type='most_productive',
            week_ending=week_ending
        ).order_by('rank')[:10],
    }
    
    context = {
        'leaderboards': leaderboards,
        'week_ending': week_ending,
    }
    return render(request, 'mortality/leaderboard.html', context)

@login_required
def anonymous_confessions(request):
    """Anonymous mortality confessions"""
    confessions = MortalityPost.objects.filter(
        post_type='confession',
        is_anonymous=True
    ).order_by('-created_at')[:20]
    
    if request.method == 'POST':
        content = request.POST.get('confession')
        if content:
            MortalityPost.objects.create(
                user=request.user,
                post_type='confession',
                title='Anonymous Confession',
                content=content,
                is_anonymous=True
            )
            messages.success(request, 'Your anonymous confession has been shared.')
            return redirect('anonymous_confessions')
    
    context = {
        'confessions': confessions,
    }
    return render(request, 'mortality/confessions.html', context)

@login_required
def mortality_stats(request):
    """Community mortality statistics"""
    from django.db.models import Avg, Count
    
    # Community stats
    total_users = User.objects.count()
    avg_life_expectancy = UserProfile.objects.aggregate(
        avg_expectancy=Avg('calculated_life_expectancy')
    )['avg_expectancy'] or 0
    
    total_time_wasted = TimeWasteEntry.objects.aggregate(
        total_hours=models.Sum('hours_per_day')
    )['total_hours'] or 0
    
    # Age group breakdown - simplified for SQLite compatibility
    from datetime import date
    current_year = date.today().year
    
    # Calculate age groups manually since SQLite doesn't support complex date functions
    profiles = UserProfile.objects.all()
    age_groups_dict = {}
    
    for profile in profiles:
        age = current_year - profile.birth_date.year
        age_group = (age // 10) * 10  # Round down to nearest 10
        age_groups_dict[age_group] = age_groups_dict.get(age_group, 0) + 1
    
    # Convert to list format for template
    age_groups = [
        {'age_group': age_group, 'count': count}
        for age_group, count in sorted(age_groups_dict.items())
    ]
    
    context = {
        'total_users': total_users,
        'avg_life_expectancy': round(avg_life_expectancy, 1),
        'total_time_wasted': round(total_time_wasted, 1),
        'age_groups': age_groups,
    }
    return render(request, 'mortality/community_stats.html', context)
