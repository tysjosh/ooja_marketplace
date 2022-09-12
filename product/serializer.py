from rest_framework import serializers
from .models import Product, Store, ProductImage


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id','name','owner','description','created_at','last_modified', 'street_1',
                    'street_2','city','state','zip_code','country','location']

        extra_kwargs = {"location": {"read_only": True}}

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','store','created_at','last_modified','store_price','sale_price',]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product',]