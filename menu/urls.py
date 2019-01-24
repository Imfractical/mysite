"""menu app URL routes"""

from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
    path('', views.list_menus, name='list_menus'),
    path('menu/<int:menu_pk>/', views.detail_menu, name='detail_menu'),
    path('menu/<int:menu_pk>/edit/', views.edit_menu, name='edit_menu'),
    path('menu/item/<int:item_pk>/', views.detail_item, name='detail_item'),
    path('menu/new/', views.create_menu, name='create_menu'),
]
