import datetime

from django import forms

from .models import Dish, Ingredient, Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('season', 'expiration_date', 'dishes')

    def clean_expiration_date(self):
        date = self.cleaned_data['expiration_date']
        if date:
            if date <= datetime.date.today():
                raise forms.ValidationError('Expiration date must be in the future!')

        return date


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ('name', 'description', 'standard', 'ingredients')


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name',)
