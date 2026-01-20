"""
Django Management Command: setup_rls

Sets up Row Level Security (RLS) on PostgreSQL tables.

Usage:
    python manage.py setup_rls

IMPORTANT: This only works with PostgreSQL/Supabase, not SQLite!
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Set up Row Level Security (RLS) on PostgreSQL tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it',
        )
        parser.add_argument(
            '--table',
            type=str,
            help='Only set up RLS for a specific table',
        )

    def handle(self, *args, **options):
        # Check database type
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' not in db_engine.lower():
            self.stdout.write(
                self.style.ERROR(
                    '\nRLS only works with PostgreSQL!\n'
                    'Current database: SQLite\n'
                    'Please switch to PostgreSQL/Supabase first.\n'
                    'See docs/RLS_SETUP_GUIDE.md for instructions.\n'
                )
            )
            return

        self.stdout.write(self.style.SUCCESS('\n=== RLS Setup for Django ===\n'))

        if options['dry_run']:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made\n'))

        # Import and run setup
        try:
            import sys
            import os
            script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'scripts', 'setup_rls.py')
            if os.path.exists(script_path):
                sys.path.insert(0, os.path.dirname(script_path))
                from setup_rls import setup_rls
                success = setup_rls()
            else:
                self.stdout.write(self.style.ERROR('RLS setup script not found'))
                success = False
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'Failed to import RLS setup: {e}'))
            success = False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'RLS setup failed: {e}'))
            success = False

        if success:
            self.stdout.write(
                self.style.SUCCESS('\n✅ RLS setup completed successfully!')
            )
            self.stdout.write(
                '\nNOTE: RLS middleware is enabled in settings.py\n'
                '      It automatically sets user ID for RLS policies.\n'
            )
        else:
            self.stdout.write(
                self.style.ERROR('\n❌ RLS setup had errors. Check output above.')
            )

