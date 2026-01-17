# Generated migration for MealPlan model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipeimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Date for this meal plan')),
                ('meal_type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('snack', 'Snack'), ('dessert', 'Dessert')], default='dinner', help_text='Type of meal (breakfast, lunch, dinner, snack, dessert)', max_length=20)),
                ('notes', models.TextField(blank=True, help_text='Optional notes for this meal plan', max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipe', models.ForeignKey(help_text='Recipe planned for this meal', on_delete=django.db.models.deletion.CASCADE, related_name='meal_plans', to='recipes.recipe')),
                ('user', models.ForeignKey(help_text='User who created this meal plan', on_delete=django.db.models.deletion.CASCADE, related_name='meal_plans', to='users.customuser')),
            ],
            options={
                'verbose_name': 'Meal Plan',
                'verbose_name_plural': 'Meal Plans',
                'ordering': ['date', 'meal_type'],
            },
        ),
        migrations.AddIndex(
            model_name='mealplan',
            index=models.Index(fields=['user', 'date'], name='recipes_meal_user_id_7a8b2a_idx'),
        ),
        migrations.AddIndex(
            model_name='mealplan',
            index=models.Index(fields=['date', 'meal_type'], name='recipes_meal_date_8c9d4e_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='mealplan',
            unique_together={('user', 'date', 'meal_type')},
        ),
    ]

