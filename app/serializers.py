from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User

class productserializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    # id = serializers.ReadOnlyField()
    class Meta:
        model = product
        fields = '__all__'
        # fields = ('product_name','product_price')
class subcatserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=sub_cat
        fields='__all__'

class Userserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
class reviewserializer(serializers.Serializer):
    review = serializers.CharField(max_length=100)
    rating = serializers.IntegerField()
    product_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    # class Meta:
    #     model = reviews
    #     fields = ['product_id', 'review','rating']

# class ProductsSerializer(serializers.Serializer):
#     product_name=serializers.CharField(max_lenght=100)
  

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = cat
        fields = '__all__'
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductImage
        # fields = ['id','image','product_detail']
        fields='__all__'


class SubCategoryByCategory(serializers.ModelSerializer):
    class Meta:
        model = sub_cat
        fields = '__all__'