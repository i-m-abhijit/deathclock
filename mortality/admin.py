from django.contrib import admin
from .models import UserProfile, TimeWasteCategory, TimeWasteEntry, MortalityReflection

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'age', 'life_expectancy', 'days_lived', 'estimated_days_remaining']
    list_filter = ['gender', 'smoking_status', 'exercise_frequency', 'created_at']
    search_fields = ['user__username', 'user__email', 'country']
    readonly_fields = ['created_at', 'calculated_life_expectancy']

@admin.register(TimeWasteCategory)
class TimeWasteCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'color']
    search_fields = ['name']

@admin.register(TimeWasteEntry)
class TimeWasteEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'hours_per_day', 'days_wasted_lifetime', 'date_logged']
    list_filter = ['category', 'date_logged']
    search_fields = ['user__username', 'category__name']
    readonly_fields = ['date_logged']

@admin.register(MortalityReflection)
class MortalityReflectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'reflection_preview']
    list_filter = ['created_at']
    search_fields = ['user__username', 'reflection_text']
    readonly_fields = ['created_at']
    
    def reflection_preview(self, obj):
        return obj.reflection_text[:100] + "..." if len(obj.reflection_text) > 100 else obj.reflection_text
    reflection_preview.short_description = 'Reflection Preview'