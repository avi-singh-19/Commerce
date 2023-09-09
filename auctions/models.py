from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category_name}"


class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='user_bid', null=True)

    def __str__(self):
        return f"{self.bid})"


class Listing(models.Model):
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, related_name='bid_price', null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', blank=True, null=True)
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title})"


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter', blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing', blank=True, null=True)
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.commenter} commented {self.message} on {self.listing}"
