from rest_framework import serializers
from product_app.models import product, Category

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['slug']
        
class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        exclude = ['slug']