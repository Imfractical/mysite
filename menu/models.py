"""menu app model definitions"""

import datetime

from django.db import models


class Menu(models.Model):
    dishes = models.ManyToManyField('Dish', related_name='dishes')
    season = models.CharField(max_length=200)
    created_date = models.DateField(null=True, default=datetime.date.today)
    expiration_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['expiration_date', 'created_date', 'season']

    def __str__(self):
        return self.season


class Dish(models.Model):
    chef = models.ForeignKey('auth.User', models.CASCADE)
    ingredients = models.ManyToManyField('Ingredient', related_name='ingredients')
    created_date = models.DateField(null=True, default=datetime.date.today)
    name = models.CharField(max_length=200)
    description = models.TextField()
    standard = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
