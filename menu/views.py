from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import DishForm, IngredientForm, MenuForm
from .models import Dish, Menu


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome, {}!".format(user.first_name))
            return redirect('menu:list')
        else:
            messages.error("Invalid login")

    return render(request, 'menu/login.html')


def signout(request):
    logout(request)
    messages.success(request, "Goodbye!")

    return redirect('menu:list')


def create_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()

            return redirect('menu:detail_menu', id=menu.pk)
    else:
        form = MenuForm()

    return render(request, 'menu/create_menu.html', {'form': form})


def create_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.chef = request.user
            dish.save()

            return redirect('menu:detail_dish', id=dish.pk)
    else:
        form = DishForm()

    return render(request, 'menu/create_dish.html', {'form': form})


def create_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()

            return redirect('menu:create_ingredient')
    else:
        form = IngredientForm()

    return render(request, 'menu/create_ingredient.html', {'form': form})


def list_menus(request):
    menus = Menu.objects.filter(
        Q(expiration_date__gte=timezone.now())
        | Q(expiration_date__isnull=True)
    )

    return render(request, 'menu/list_menus.html', {'menus': menus})


def detail_menu(request, menu_pk):
    menu = get_object_or_404(Menu, id=menu_pk)

    return render(request, 'menu/detail_menu.html', {'menu': menu})


def edit_menu(request, menu_pk):
    menu = get_object_or_404(Menu, id=menu_pk)
    dishes = Dish.objects.all()
    if request.method == 'POST':
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.strptime(
            request.POST.get('expiration_date', ''),
            '%m/%d/%Y',
        )
        menu.dishes = request.POST.get('dishes', '')
        menu.save()

    return render(request, 'menu/edit_menu.html', {
        'menu': menu,
        'dishes': dishes,
    })


def detail_dish(request, dish_pk):
    dish = get_object_or_404(Dish, id=dish_pk)

    return render(request, 'menu/detail_dish.html', {'dish': dish})
