from home.models import *
from django.db import models


# Create your models here.
class Wishlist(models.Model):
    username = models.CharField(max_length=500)
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    slug = models.CharField(max_length=300)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return self.username
