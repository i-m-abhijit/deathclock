from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('setup/', views.setup_profile, name='setup_profile'),
    path('time-waste/', views.time_waste_tracker, name='time_waste_tracker'),
    path('reflections/', views.mortality_reflection, name='mortality_reflection'),
    path('life-visualization/', views.life_visualization, name='life_visualization'),
    
    # Mortality Social Network URLs
    path('social/', views.social_feed, name='social_feed'),
    path('social/post/', views.create_post, name='create_post'),
    path('challenges/', views.mortality_challenges, name='mortality_challenges'),
    path('challenges/join/<int:challenge_id>/', views.join_challenge, name='join_challenge'),
    path('leaderboard/', views.mortality_leaderboard, name='mortality_leaderboard'),
    path('confessions/', views.anonymous_confessions, name='anonymous_confessions'),
    path('community-stats/', views.mortality_stats, name='mortality_stats'),
]