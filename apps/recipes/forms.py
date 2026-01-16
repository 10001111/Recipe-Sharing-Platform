"""
Forms for Recipe Management

Forms for creating and editing recipes
"""

from django import forms
from .models import Recipe, Category, Ingredient, RecipeIngredient, Rating, Comment


class RecipeForm(forms.ModelForm):
    """Form for creating/editing recipes"""
    
    # Ingredients will be handled separately via formset
    ingredients_data = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        help_text="JSON data for ingredients"
    )
    
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'instructions',
            'prep_time',
            'cook_time',
            'image',
            'category',
            'dietary_restrictions',
            'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Brief description of the recipe'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Step-by-step cooking instructions'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Minutes'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Minutes'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        help_texts = {
            'prep_time': 'Preparation time in minutes',
            'cook_time': 'Cooking time in minutes',
            'image': 'Upload a photo of your recipe',
            'is_published': 'Make this recipe visible to others',
        }


class RecipeIngredientForm(forms.ModelForm):
    """Form for adding ingredients to a recipe"""
    
    ingredient_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingredient name (e.g., Flour, Sugar)'
        }),
        help_text="Ingredient name"
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'unit', 'notes']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'placeholder': 'Quantity'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unit (e.g., cups, tbsp, grams, pieces)'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional notes (e.g., chopped, diced)'
            }),
        }
    
    def save(self, commit=True, recipe=None, ingredient=None):
        """Save the RecipeIngredient with recipe and ingredient"""
        instance = super().save(commit=False)
        if recipe:
            instance.recipe = recipe
        if ingredient:
            instance.ingredient = ingredient
        if commit:
            instance.save()
        return instance


class RecipeIngredientFormSet(forms.BaseFormSet):
    """FormSet for managing multiple ingredients"""
    pass


class RatingForm(forms.ModelForm):
    """Form for rating a recipe"""
    
    class Meta:
        model = Rating
        fields = ['stars', 'review_text']
        widgets = {
            'stars': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'required': True
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': 1000,
                'placeholder': 'Optional: Write a review (max 1000 characters)'
            }),
        }
        help_texts = {
            'stars': 'Rate from 1 to 5 stars',
            'review_text': 'Optional review text (max 1000 characters)',
        }
    
    def clean_stars(self):
        stars = self.cleaned_data.get('stars')
        if stars and (stars < 1 or stars > 5):
            raise forms.ValidationError('Rating must be between 1 and 5 stars.')
        return stars


class CommentForm(forms.ModelForm):
    """Form for commenting on a recipe"""
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': 1000,
                'placeholder': 'Write your comment (max 1000 characters)',
                'required': True
            }),
        }
        help_texts = {
            'text': 'Your comment (max 1000 characters)',
        }

