from django import forms

from .models import Dish, Ingredient, Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('season', 'expiration_date', 'dishes')


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ('name', 'description', 'standard', 'ingredients')


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name')
