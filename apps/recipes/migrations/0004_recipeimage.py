# Generated migration for RecipeImage model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_dietary_restrictions'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(help_text='URL from Vercel Blob Storage or other image hosting service', max_length=500)),
                ('is_primary', models.BooleanField(default=False, help_text='Primary/featured image for the recipe')),
                ('order', models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')),
                ('alt_text', models.CharField(blank=True, help_text='Alt text for accessibility', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipe', models.ForeignKey(help_text='Recipe this image belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'Recipe Image',
                'verbose_name_plural': 'Recipe Images',
                'ordering': ['order', 'created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='recipeimage',
            constraint=models.UniqueConstraint(condition=models.Q(('is_primary', True)), fields=('recipe', 'is_primary'), name='unique_primary_image_per_recipe'),
        ),
    ]

