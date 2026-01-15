"""
Management command to load sample data fixtures

Usage:
    python manage.py load_sample_data
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Load sample data fixtures into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fixture',
            type=str,
            default='sample_data.json',
            help='Fixture file name (default: sample_data.json)'
        )

    def handle(self, *args, **options):
        fixture_name = options['fixture']
        fixture_path = os.path.join(
            settings.BASE_DIR,
            'apps',
            'recipes',
            'fixtures',
            fixture_name
        )

        if not os.path.exists(fixture_path):
            self.stdout.write(
                self.style.ERROR(
                    f'Fixture file not found: {fixture_path}'
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'Loading fixture: {fixture_name}')
        )

        try:
            call_command('loaddata', fixture_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully loaded {fixture_name}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading fixture: {str(e)}')
            )

