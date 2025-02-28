from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User


class productserializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
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