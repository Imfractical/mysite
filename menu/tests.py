import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import MenuForm
from .models import Dish, Ingredient, Menu


class MenuTests(TestCase):
    def setUp(self):
        chef = User.objects.create_user(username='bobone', first_name='Bob', last_name='Stud')

        papaya = Ingredient.objects.create(name='Papaya')
        orange = Ingredient.objects.create(name='Orange')
        fish = Ingredient.objects.create(name='Fish')

        fruity_fish = Dish()
        fruity_fish.chef = chef
        fruity_fish.name = 'Fruity Fish'
        fruity_fish.description = 'Yum!'
        fruity_fish.standard = True
        fruity_fish.save()
        fruity_fish.ingredients.add(papaya, orange, fish)

        fishie = Dish()
        fishie.chef = chef
        fishie.name = 'Fishie'
        fishie.description = "Plain ol' fish"
        fishie.save()
        fishie.ingredients.add(fish)

        both_fishes = Menu()
        both_fishes.season = 'Both Fishies'
        both_fishes.chef = chef
        both_fishes.save()
        both_fishes.dishes.add(fruity_fish, fishie)

        one_fish = Menu()
        one_fish.season = 'Just One :('
        one_fish.chef = chef
        one_fish.expiration_date = datetime.date(year=2030, month=3, day=1)
        one_fish.save()
        one_fish.dishes.add(fishie)

    def test_models_return_name_as_string(self):
        papaya = Ingredient.objects.get(name='Papaya')
        fruity_fish = Dish.objects.get(name='Fruity Fish')
        both_fishes = Menu.objects.get(season='Both Fishies')

        self.assertEqual(str(papaya), 'Papaya')
        self.assertEqual(str(fruity_fish), 'Fruity Fish')
        self.assertEqual(str(both_fishes), 'Both Fishies')

    def test_menu_form_expiration_date_in_future(self):
        menu1 = MenuForm(data={
            'season': 'April',
            'dishes': [Dish.objects.get(name='Fruity Fish')],
            'expiration_date': datetime.date(year=1980, month=1, day=1),
        })
        menu1.save()

        self.assertFalse(menu1.is_valid())
