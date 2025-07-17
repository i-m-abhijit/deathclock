from django.core.management.base import BaseCommand
from mortality.models import TimeWasteCategory

class Command(BaseCommand):
    help = 'Populate initial time waste categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Social Media Scrolling',
                'description': 'Mindlessly scrolling through feeds, watching others live their lives',
                'color': '#ff4444'
            },
            {
                'name': 'Television/Netflix',
                'description': 'Passive consumption of entertainment, living vicariously through fictional characters',
                'color': '#ff6b6b'
            },
            {
                'name': 'Video Games',
                'description': 'Escaping reality through virtual achievements that mean nothing',
                'color': '#ff9999'
            },
            {
                'name': 'Procrastination',
                'description': 'Avoiding important tasks, delaying your potential',
                'color': '#ffcccc'
            },
            {
                'name': 'Mindless Web Browsing',
                'description': 'Clicking from link to link with no purpose or goal',
                'color': '#cc0000'
            },
            {
                'name': 'Gossip/Drama',
                'description': 'Wasting energy on other people\'s business instead of your own',
                'color': '#990000'
            },
            {
                'name': 'Excessive Sleep',
                'description': 'Sleeping more than 8 hours, hiding from life in unconsciousness',
                'color': '#660000'
            },
            {
                'name': 'Complaining',
                'description': 'Focusing on problems without taking action to solve them',
                'color': '#330000'
            }
        ]

        for cat_data in categories:
            category, created = TimeWasteCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'color': cat_data['color']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated time waste categories')
        )