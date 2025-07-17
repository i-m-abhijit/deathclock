from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile, TimeWasteEntry, TimeWasteCategory, MortalityReflection
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
