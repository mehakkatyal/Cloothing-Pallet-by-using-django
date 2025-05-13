from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User


class OrderSeriaizer(serializers.ModelSerializer):
    class Meta:
        model=ordernow
        fields='__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProductImage
        # fields = ['id','image','product_detail']
        fields='__all__'

class productserializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    # id = serializers.ReadOnlyField()
    images=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model = product
        fields = '__all__'
        # fields = ('product_name','product_price')
class subcatserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=sub_cat
        fields='__all__'
        
class Userprofileserializer(serializers.ModelSerializer):
    
    class Meta:
         model=userprofile
         fields=['phonenumber','is_vendor','user']

# class Userserializer(serializers.ModelSerializer):
#     userprofile=Userprofileserializer()
#     class Meta:
#         model=User
#         fields=['username','password','first_name','last_name','email','userprofile']
class UserSerializer(serializers.ModelSerializer):
    phonenumber = serializers.CharField(source="userprofile.phonenumber", required=False)
    is_vendor = serializers.BooleanField(source="userprofile.is_vendor", required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'phonenumber', 'is_vendor']
   



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



class SubCategoryByCategory(serializers.ModelSerializer):
    class Meta:
        model = sub_cat
        fields = '__all__'
class ProductBysubcategory(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model=product
        # fields = ['product_name','images','product_price']
        fields='__all__'