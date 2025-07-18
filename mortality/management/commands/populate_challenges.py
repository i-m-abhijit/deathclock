from django.core.management.base import BaseCommand
from mortality.models import MortalityChallenge
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate initial mortality challenges'

    def handle(self, *args, **options):
        # Get or create admin user for challenges
        admin_user, created = User.objects.get_or_create(
            username='deathclock_admin',
            defaults={'email': 'admin@deathclock.com', 'is_staff': True}
        )
        
        challenges = [
            {
                'title': '30-Day Social Media Detox',
                'description': 'Reduce social media usage by 50% for 30 days. Reclaim hours of your precious life from mindless scrolling.',
                'challenge_type': 'time_waste',
                'duration_days': 30,
                'points_reward': 300,
            },
            {
                'title': 'Learn Something New Before You Die',
                'description': 'Dedicate 1 hour daily to learning a new skill. Your time is limited - use it to grow.',
                'challenge_type': 'learning',
                'duration_days': 30,
                'points_reward': 250,
            },
            {
                'title': 'Strengthen One Relationship',
                'description': 'Reach out to someone important daily. You never know how much time you have left with them.',
                'challenge_type': 'relationships',
                'duration_days': 14,
                'points_reward': 200,
            },
            {
                'title': 'Eliminate One Time Waster',
                'description': 'Identify your biggest time waster and eliminate it completely. Every minute counts.',
                'challenge_type': 'time_waste',
                'duration_days': 21,
                'points_reward': 275,
            },
            {
                'title': 'Daily Mortality Reflection',
                'description': 'Spend 10 minutes daily reflecting on your mortality and life priorities. Face the truth.',
                'challenge_type': 'productivity',
                'duration_days': 7,
                'points_reward': 150,
            },
            {
                'title': 'Health Improvement Challenge',
                'description': 'Exercise 30 minutes daily. Your body is the only one you get - make it last.',
                'challenge_type': 'health',
                'duration_days': 30,
                'points_reward': 350,
            },
            {
                'title': 'Productivity Power Week',
                'description': 'Track and optimize every hour for 7 days. See how much time you actually waste.',
                'challenge_type': 'productivity',
                'duration_days': 7,
                'points_reward': 175,
            },
            {
                'title': 'Digital Sunset Challenge',
                'description': 'No screens 2 hours before bed for 14 days. Reclaim your evenings and sleep.',
                'challenge_type': 'health',
                'duration_days': 14,
                'points_reward': 225,
            }
        ]

        for challenge_data in challenges:
            challenge, created = MortalityChallenge.objects.get_or_create(
                title=challenge_data['title'],
                defaults={
                    'description': challenge_data['description'],
                    'challenge_type': challenge_data['challenge_type'],
                    'duration_days': challenge_data['duration_days'],
                    'points_reward': challenge_data['points_reward'],
                    'created_by': admin_user,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created challenge: {challenge.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Challenge already exists: {challenge.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated mortality challenges')
        )