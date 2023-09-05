from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category_name}"


class Listing(models.Model):
    price = models.FloatField()
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title})"
