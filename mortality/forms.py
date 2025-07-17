from django import forms
from .models import UserProfile, TimeWasteEntry, MortalityReflection
from datetime import date

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'birth_date', 'gender', 'country', 'smoking_status', 'drinking_habits',
            'exercise_frequency', 'bmi_category', 'sleep_quality', 'family_longevity',
            'stress_level', 'social_connections'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'max': date.today().isoformat()
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., United States, Japan, Germany'
            }),
            'smoking_status': forms.Select(attrs={'class': 'form-control'}),
            'drinking_habits': forms.Select(attrs={'class': 'form-control'}),
            'exercise_frequency': forms.Select(attrs={'class': 'form-control'}),
            'bmi_category': forms.Select(attrs={'class': 'form-control'}),
            'sleep_quality': forms.Select(attrs={'class': 'form-control'}),
            'family_longevity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 40,
                'max': 120,
                'value': 75
            }),
            'stress_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'value': 5
            }),
            'social_connections': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'birth_date': 'When did your countdown begin?',
            'gender': 'Gender',
            'country': 'Country of residence',
            'smoking_status': 'Smoking habits',
            'drinking_habits': 'Alcohol consumption',
            'exercise_frequency': 'Exercise frequency',
            'bmi_category': 'BMI category',
            'sleep_quality': 'Sleep quality',
            'family_longevity': 'Family longevity (average age of death)',
            'stress_level': 'Stress level (1-10)',
            'social_connections': 'Do you have strong social connections?'
        }

class TimeWasteEntryForm(forms.ModelForm):
    class Meta:
        model = TimeWasteEntry
        fields = ['category', 'hours_per_day', 'notes']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'hours_per_day': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 24,
                'step': 0.5
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Justify your waste of precious time...'
            })
        }
        labels = {
            'category': 'How are you wasting your life?',
            'hours_per_day': 'Hours per day (be honest)',
            'notes': 'Excuses and justifications'
        }

class ReflectionForm(forms.ModelForm):
    class Meta:
        model = MortalityReflection
        fields = ['reflection_text']
        widgets = {
            'reflection_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'What does your mortality mean to you? How will you change?'
            })
        }
        labels = {
            'reflection_text': 'Your mortality reflection'
        }