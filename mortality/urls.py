from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('setup/', views.setup_profile, name='setup_profile'),
    path('time-waste/', views.time_waste_tracker, name='time_waste_tracker'),
    path('reflections/', views.mortality_reflection, name='mortality_reflection'),
    path('life-visualization/', views.life_visualization, name='life_visualization'),
]