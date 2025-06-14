# home/serializers.py
from rest_framework import serializers
from .models import PotteryCategory, Product

class PotteryCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for PotteryCategory model, using correct fields.
    """
    name = serializers.CharField()  # Explicitly map name
    image = serializers.PrimaryKeyRelatedField(
        queryset='wagtailimages.Image.objects.all()',  # Or use a nested serializer if needed
        allow_null=True
    )

    class Meta:
        model = PotteryCategory
        fields = ['id', 'name', 'image']

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model, including nested PotteryCategory data.
    """
    category = PotteryCategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'intro', 'category', 'price']