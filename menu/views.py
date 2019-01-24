from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MenuForm
from .models import Item, Menu


def create_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()

            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()

    return render(request, 'menu/create_menu.html', {'form': form})


def list_menus(request):
    menus = Menu.objects.filter(
        Q(expiration_date__gte=timezone.now())
        | Q(expiration_date__isnull=True)
    )

    return render(request, 'menu/list_menus.html', {'menus': menus})


def detail_menu(request, menu_pk):
    menu = Menu.objects.get(pk=menu_pk)

    return render(request, 'menu/detail_menu.html', {'menu': menu})


def edit_menu(request, menu_pk):
    menu = get_object_or_404(Menu, pk=menu_pk)
    items = Item.objects.all()
    if request.method == 'POST':
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.strptime(
            request.POST.get('expiration_date', ''),
            '%m/%d/%Y',
        )
        menu.items = request.POST.get('items', '')
        menu.save()

    return render(request, 'menu/edit_menu.html', {
        'menu': menu,
        'items': items,
    })


def detail_item(request, item_pk):
    try:
        item = Item.objects.get(pk=item_pk)
    except ObjectDoesNotExist:
        raise Http404

    return render(request, 'menu/detail_item.html', {'item': item})
