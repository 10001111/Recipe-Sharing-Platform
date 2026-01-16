# Generated manually for adding dietary_restrictions field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_recipe_view_count_rating_favorite_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='dietary_restrictions',
            field=models.CharField(
                choices=[
                    ('none', 'No dietary restrictions'),
                    ('vegetarian', 'Vegetarian'),
                    ('vegan', 'Vegan'),
                    ('gluten-free', 'Gluten-Free'),
                    ('keto', 'Keto'),
                    ('paleo', 'Paleo'),
                    ('pescatarian', 'Pescatarian'),
                    ('halal', 'Halal'),
                    ('kosher', 'Kosher'),
                ],
                default='none',
                help_text='Dietary restrictions for this recipe',
                max_length=20
            ),
        ),
    ]

