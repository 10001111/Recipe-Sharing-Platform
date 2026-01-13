"""
Django management command to create default recipe categories

Usage:
    python manage.py create_categories
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.recipes.models import Category


class Command(BaseCommand):
    help = 'Creates default recipe categories'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Breakfast', 'description': 'Morning meals and breakfast recipes'},
            {'name': 'Lunch', 'description': 'Midday meals and lunch recipes'},
            {'name': 'Dinner', 'description': 'Evening meals and dinner recipes'},
            {'name': 'Dessert', 'description': 'Sweet treats and dessert recipes'},
            {'name': 'Snack', 'description': 'Quick snacks and appetizers'},
            {'name': 'Beverage', 'description': 'Drinks and beverages'},
            {'name': 'Soup', 'description': 'Soups and stews'},
            {'name': 'Salad', 'description': 'Salads and fresh dishes'},
            {'name': 'Vegetarian', 'description': 'Vegetarian recipes'},
            {'name': 'Vegan', 'description': 'Vegan recipes'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for cat_data in categories:
            slug = slugify(cat_data['name'])
            # Try to get by slug first, then by name
            try:
                category = Category.objects.get(slug=slug)
                created = False
            except Category.DoesNotExist:
                try:
                    category = Category.objects.get(name=cat_data['name'])
                    # Update slug if missing
                    if not category.slug:
                        category.slug = slug
                        category.save()
                    created = False
                except Category.DoesNotExist:
                    category = Category.objects.create(
                        name=cat_data['name'],
                        slug=slug,
                        description=cat_data['description']
                    )
                    created = True
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
                created_count += 1
            else:
                # Update description if different
                if category.description != cat_data['description']:
                    category.description = cat_data['description']
                    category.save()
                    self.stdout.write(
                        self.style.WARNING(f'Updated category: {category.name}')
                    )
                    updated_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Category already exists: {category.name}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: Created {created_count} categories, {updated_count} updated'
            )
        )

