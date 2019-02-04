import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import MenuForm
from .models import Dish, Ingredient, Menu


class MenuTests(TestCase):
    def setUp(self):
        User.objects.create_user('Crampy', password='sixlicks')

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
        menu2 = MenuForm(data={
            'season': 'Smash Mouth',
            'dishes': [Dish.objects.get(name='Fruity Fish'), Dish.objects.get(name='Fishie')],
            'expiration_date': datetime.date(year=2030, month=1, day=1),
        })

        self.assertFalse(menu1.is_valid())
        self.assertTrue(menu2.is_valid())

    def test_signin_view(self):
        response = self.client.post(reverse('menu:login'), {'username': 'Crampy', 'password': 'sixlicks'}, follow=True)

        self.assertTrue(response.context['user'].is_active)

    def test_signout_view(self):
        self.client.login(username='Crampy', password='sixlicks')
        response = self.client.get(reverse('menu:logout'))

        self.assertEqual(response.status_code, 302)

    def test_create_menu_view(self):
        self.client.login(username='Crampy', password='sixlicks')
        response = self.client.post(reverse('menu:create_menu'), {
            'season': 'yep',
            'dishes': [Dish.objects.get(name='Fruity Fish')],
            'expiration_date': datetime.date(year=2040, month=12, day=12),
        })

        self.assertEqual(response.status_code, 200)

    def test_create_dish_view(self):
        self.client.login(username='Crampy', password='sixlicks')
        response = self.client.post(reverse('menu:create_dish'), {
            'name': 'skip',
            'ingredients': [Ingredient.objects.get(name='Papaya')],
            'description': 'spicy',
            'standard': True,
        })

        self.assertEqual(response.status_code, 200)

    def test_create_ingredient_view(self):
        self.client.login(username='Crampy', password='sixlicks')
        response = self.client.post(reverse('menu:create_ingredient'), {
            'name': 'spazzle',
        })

        self.assertEqual(response.status_code, 302)

    def test_list_menus_view(self):
        response = self.client.get(reverse('menu:list_menus'))

        self.assertContains(response, 'Both Fishies')
        self.assertContains(response, 'Just One :(')

    def test_list_ingredients_view(self):
        response = self.client.get(reverse('menu:list_ingredients'))

        self.assertContains(response, 'Papaya')
        self.assertContains(response, 'Orange')
        self.assertContains(response, 'Fish')

    def test_detail_menu_view(self):
        menu = Menu.objects.get(season='Both Fishies')
        response = self.client.get(reverse('menu:detail_menu', args=[menu.id]))

        self.assertContains(response, 'Fruity Fish')
        self.assertContains(response, 'Fishie')

    def test_detail_dish_view(self):
        dish = Dish.objects.get(name='Fruity Fish')
        response = self.client.get(reverse('menu:detail_dish', args=[dish.id]))

        self.assertContains(response, 'Yum!')

    def test_edit_menu_view(self):
        self.client.login(username='Crampy', password='sixlicks')
        menu = Menu.objects.get(season='Both Fishies')
        response = self.client.post(reverse('menu:edit_menu', args=[menu.id]), {
            'season': 'pep',
        })

        self.assertEqual(response.status_code, 200)

    def test_edit_dish_view(self):
        self.client.login(username='Crampy', password='sixlicks')
        dish = Dish.objects.get(name='Fruity Fish')
        response = self.client.post(reverse('menu:edit_dish', args=[dish.id]), {
            'name': 'skip',
        })

        self.assertEqual(response.status_code, 200)

    def test_edit_ingredient_view(self):
        self.client.login(username='Crampy', password='sixlicks')
        ingredient = Ingredient.objects.get(name='Papaya')
        response = self.client.post(reverse('menu:edit_ingredient', args=[ingredient.id]), {
            'name': 'dazzle',
        })

        self.assertEqual(response.status_code, 302)
