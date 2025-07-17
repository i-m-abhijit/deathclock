from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
import calendar


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    SMOKING_CHOICES = [
        ('never', 'Never smoked'),
        ('former', 'Former smoker'),
        ('light', 'Light smoker (1-10/day)'),
        ('moderate', 'Moderate smoker (11-20/day)'),
        ('heavy', 'Heavy smoker (20+/day)'),
    ]

    DRINKING_CHOICES = [
        ('none', 'No alcohol'),
        ('light', 'Light (1-3 drinks/week)'),
        ('moderate', 'Moderate (4-14 drinks/week)'),
        ('heavy', 'Heavy (15+ drinks/week)'),
    ]

    EXERCISE_CHOICES = [
        ('none', 'No regular exercise'),
        ('light', 'Light (1-2 times/week)'),
        ('moderate', 'Moderate (3-4 times/week)'),
        ('heavy', 'Heavy (5+ times/week)'),
    ]

    BMI_CHOICES = [
        ('underweight', 'Underweight (BMI < 18.5)'),
        ('normal', 'Normal (BMI 18.5-24.9)'),
        ('overweight', 'Overweight (BMI 25-29.9)'),
        ('obese', 'Obese (BMI 30+)'),
    ]

    SLEEP_CHOICES = [
        ('poor', 'Poor (< 6 hours)'),
        ('fair', 'Fair (6-7 hours)'),
        ('good', 'Good (7-9 hours)'),
        ('excessive', 'Excessive (9+ hours)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='M')
    country = models.CharField(max_length=100, default='India')

    # Health factors
    smoking_status = models.CharField(
        max_length=10, choices=SMOKING_CHOICES, default='never')
    drinking_habits = models.CharField(
        max_length=10, choices=DRINKING_CHOICES, default='none')
    exercise_frequency = models.CharField(
        max_length=10, choices=EXERCISE_CHOICES, default='none')
    bmi_category = models.CharField(
        max_length=15, choices=BMI_CHOICES, default='normal')
    sleep_quality = models.CharField(
        max_length=10, choices=SLEEP_CHOICES, default='good')

    # Family history
    family_longevity = models.IntegerField(
        default=75, help_text="Average age of death of parents/grandparents")

    # Lifestyle
    stress_level = models.IntegerField(
        default=5, help_text="Stress level 1-10 (10 being extremely stressed)")
    social_connections = models.BooleanField(
        default=True, help_text="Do you have strong social connections?")

    # Calculated field
    calculated_life_expectancy = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_life_expectancy(self):
        """Calculate life expectancy based on various factors"""
        # Base life expectancy by country (simplified)
        base_expectancy = {
            'Japan': 84.6,
            'Switzerland': 83.8,
            'Singapore': 83.6,
            'Australia': 83.4,
            'Spain': 83.4,
            'Iceland': 83.0,
            'Italy': 83.0,
            'Israel': 82.8,
            'Sweden': 82.8,
            'France': 82.7,
            'South Korea': 82.7,
            'Canada': 82.4,
            'Norway': 82.3,
            'Luxembourg': 82.3,
            'Netherlands': 82.3,
            'Finland': 81.9,
            'Austria': 81.6,
            'United Kingdom': 81.3,
            'Belgium': 81.8,
            'Germany': 81.3,
            'Ireland': 82.3,
            'United States': 78.9,
            'China': 77.3,
            'Russia': 72.6,
            'India': 69.7,
        }

        base = base_expectancy.get(self.country, 78.9)

        # Gender adjustment
        if self.gender == 'F':
            base += 5  # Women typically live 5 years longer
        elif self.gender == 'M':
            base -= 2  # Men typically live 2 years less than average

        # Smoking adjustments
        smoking_impact = {
            'never': 0,
            'former': -2,
            'light': -5,
            'moderate': -8,
            'heavy': -12
        }
        base += smoking_impact.get(self.smoking_status, 0)

        # Drinking adjustments
        drinking_impact = {
            'none': 0,
            'light': 1,  # Light drinking can be beneficial
            'moderate': -1,
            'heavy': -6
        }
        base += drinking_impact.get(self.drinking_habits, 0)

        # Exercise adjustments
        exercise_impact = {
            'none': -3,
            'light': 1,
            'moderate': 3,
            'heavy': 5
        }
        base += exercise_impact.get(self.exercise_frequency, 0)

        # BMI adjustments
        bmi_impact = {
            'underweight': -2,
            'normal': 0,
            'overweight': -2,
            'obese': -6
        }
        base += bmi_impact.get(self.bmi_category, 0)

        # Sleep adjustments
        sleep_impact = {
            'poor': -4,
            'fair': -1,
            'good': 0,
            'excessive': -2
        }
        base += sleep_impact.get(self.sleep_quality, 0)

        # Family history (genetics)
        genetic_factor = (self.family_longevity - 75) * 0.3
        base += genetic_factor

        # Stress level impact
        stress_impact = (self.stress_level - 5) * -0.5
        base += stress_impact

        # Social connections
        if not self.social_connections:
            base -= 4

        # Ensure reasonable bounds
        base = max(50, min(120, base))

        self.calculated_life_expectancy = round(base, 1)
        return self.calculated_life_expectancy

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def days_lived(self):
        return (date.today() - self.birth_date).days

    @property
    def life_expectancy(self):
        """Get the calculated life expectancy, calculating if needed"""
        if self.calculated_life_expectancy is None:
            self.calculate_life_expectancy()
            self.save()
        return self.calculated_life_expectancy

    def estimated_days_remaining(self):
        total_days = self.life_expectancy * 365.25
        return max(0, int(total_days - self.days_lived()))

    def life_percentage_lived(self):
        total_days = self.life_expectancy * 365.25
        return min(100, (self.days_lived() / total_days) * 100)

    def weeks_remaining(self):
        return self.estimated_days_remaining() // 7

    def __str__(self):
        return f"{self.user.username}'s mortality profile"


class TimeWasteCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=7, default="#ff0000")  # Hex color

    def __str__(self):
        return self.name


class TimeWasteEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(TimeWasteCategory, on_delete=models.CASCADE)
    hours_per_day = models.FloatField()
    date_logged = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def days_wasted_lifetime(self):
        if hasattr(self.user, 'userprofile'):
            profile = self.user.userprofile
            days_lived = profile.days_lived()
            return (self.hours_per_day * days_lived) / 24
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.category.name}: {self.hours_per_day}h/day"


class MortalityReflection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reflection_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s reflection - {self.created_at.strftime('%Y-%m-%d')}"
