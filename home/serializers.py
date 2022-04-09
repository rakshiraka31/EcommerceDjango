from rest_framework import serializers
from .models import Item


# Serializers define the API representation.
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'category', 'brand', 'image', 'price', 'status', 'label', 'slug']
