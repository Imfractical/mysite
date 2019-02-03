"""menu app URL routes"""

from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('', views.list_menus, name='list'),
    path('menu/new/', views.create_menu, name='create_menu'),
    path('menu/<int:menu_pk>/', views.detail_menu, name='detail_menu'),
    path('menu/<int:menu_pk>/edit/', views.edit_menu, name='edit_menu'),
    path('dish/new/', views.create_dish, name='create_dish'),
    path('dish/<int:dish_pk>/', views.detail_dish, name='detail_dish'),
    path('dish/<int:dish_pk>/edit', views.edit_dish, name='edit_dish'),
    path('ingredient/', views.list_ingredients, name='list_ingredients'),
    path('ingredient/new/', views.create_ingredient, name='create_ingredient'),
    path('ingredient/<int:ingredient_pk>/edit/', views.edit_ingredient, name='edit_ingredient'),
]
