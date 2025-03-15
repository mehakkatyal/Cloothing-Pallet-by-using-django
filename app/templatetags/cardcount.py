from django import template
from app.models import bag

register=template.Library()
@register.simple_tag
def addcart(request):
    if not request.user.is_authenticated:
        return 0
    cart_item=bag.objects.filter(user=request.user)

    return cart_item  
   
