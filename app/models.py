from django.db import models
from django.contrib.auth.models import User
import datetime

class userprofile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    is_vendor=models.BooleanField(default=False)
    phonenumber=models.CharField(max_length=11)
    def __str__(self):
        return super().__str__()
    
class cat(models.Model):
    cat_name=models.CharField(max_length=100)
    cat_pic=models.ImageField(upload_to='photo/',null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)


    def __str__(self):
        return str.title(self.cat_name)
class sub_cat(models.Model):
    cat=models.ForeignKey(cat,on_delete=models.CASCADE)
    sub_cat_name=models.CharField(max_length=100)
    sub_cat_pic=models.ImageField(upload_to='photo/',null=True,blank=True)
    

    def __str__(self):
        return self.sub_cat_name.title()
class product(models.Model):
    sub_cat=models.ForeignKey(sub_cat,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product_name= models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_dis=models.CharField(max_length=150, null=True)
    product_color=models.CharField(max_length=100, null=True)
    product_size=models.IntegerField(null=True)
    product_type=models.CharField(max_length=10,null=True)
    product_seleve=models.CharField(max_length=20,null=True)
    product_fit=models.CharField(max_length=10,null=True)
    packof=models.CharField(max_length=10,null=True)
    # quantity=models.IntegerChoices(null=True)
    fabric=models.CharField(max_length=20,null=True)
    stock=models.IntegerField(null=True)
   
    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product_detail = models.ForeignKey(product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='photo/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.ProductDetail.product.product_name}"
    
class ordernow(models.Model):
    PAYMENT_METHODS=[
        ('credit card','credit card'),
        ('phone pay','phone pay'),
        ('bank transfer','bank traansfer'),
        ('COD','COD')
    ]
    STATUS=[
        ('pending','pending'),
        ('canfirmed','canfirmed'),
        ('cancelled','cancelled')
    ]

    product=models.ForeignKey(product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.IntegerField()
    booking_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,choices=STATUS,default='pending')
    shipping_adress=models.TextField()
    payment_method=models.CharField(max_length=20,choices=PAYMENT_METHODS,null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    stock = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return str.title()
    

class bag(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qu=models.IntegerField(null=True,default=1)
    date=models.DateField(default=datetime.date.today)

    def __str__(self):
        return super().__str__()
class reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    review=models.TextField(max_length=100,null=True)
    rating=models.IntegerField()

    def __str__(self):
        return super().__str__()