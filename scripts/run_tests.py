"""
Script to run all tests for the Recipe Sharing Platform

Usage:
    python scripts/run_tests.py
"""

import os
import sys
import django

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.test.utils import get_runner
from django.conf import settings


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running Tests for Recipe Sharing Platform")
    print("=" * 70)
    print()

    # Run tests using Django test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)
    
    # Run tests for all apps
    failures = test_runner.run_tests([
        'apps.recipes.tests',
        'apps.users.tests',
    ])
    
    if failures:
        print("\n" + "=" * 70)
        print(f"Tests completed with {failures} failure(s)")
        print("=" * 70)
        sys.exit(1)
    else:
        print("\n" + "=" * 70)
        print("All tests passed!")
        print("=" * 70)
        sys.exit(0)


if __name__ == '__main__':
    run_tests()

