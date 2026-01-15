"""
Management command to run migrations

Usage:
    python manage.py run_migrations
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run all migrations for the project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fake',
            action='store_true',
            help='Mark migrations as run without actually running them'
        )
        parser.add_argument(
            '--fake-initial',
            action='store_true',
            help='Detect if tables already exist and fake-apply initial migrations'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running migrations...'))

        try:
            if options['fake']:
                call_command('migrate', '--fake')
                self.stdout.write(
                    self.style.SUCCESS('Migrations marked as applied (fake)')
                )
            elif options['fake_initial']:
                call_command('migrate', '--fake-initial')
                self.stdout.write(
                    self.style.SUCCESS('Initial migrations applied (fake-initial)')
                )
            else:
                call_command('migrate')
                self.stdout.write(
                    self.style.SUCCESS('All migrations applied successfully')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error running migrations: {str(e)}')
            )

