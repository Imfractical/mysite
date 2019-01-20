"""menu app model definitions"""

from django.db import models
from django.utils import timezone


class Menu(models.Model):
    class Meta:
        ordering = ['expiration_date', 'created_date', 'season']

    items = models.ManyToManyField('Item', related_name='items')
    season = models.CharField(max_length=20)
    created_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.season


class Item(models.Model):
    chef = models.ForeignKey('auth.User', models.CASCADE)
    ingredients = models.ManyToManyField('Ingredient')
    created_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200)
    description = models.TextField()
    standard = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
