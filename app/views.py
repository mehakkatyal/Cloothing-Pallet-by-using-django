from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from app.models import userprofile,cat,sub_cat,product,ProductImage,ordernow,bag,reviews
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from.serializers import *
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from .serializers import ProductBysubcategory
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    try:
        profile = user.userprofile  # ✅ Correct way to access OneToOne
        return Response({
            "username": user.username,
            "is_vendor": profile.is_vendor
        })
    except userprofile.DoesNotExist:
        return Response({
            "username": user.username,
            "is_vendor": False  # default or fallback
        })


# Genric view set 

class CatBySubCat(ListAPIView):
    queryset = sub_cat.objects.all()
    serializer_class = SubCategoryByCategory

    def get(self, request, *args, **kwargs):
        _id = kwargs['id']
        sub = sub_cat.objects.filter(cat_id = _id)
        serializer=SubCategoryByCategory(sub,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    #(Retrieve function)dynamic url api

class SubCategoryByCategoryViewset(ModelViewSet):
    queryset = sub_cat.objects.all()
    serializer_class = SubCategoryByCategory

    def retrieve(self, request, *args, **kwargs):
        _id = kwargs['pk']
        sub = sub_cat.objects.filter(cat_id = _id)
        serializer=SubCategoryByCategory(sub,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class ProductBysubcategoryViewet(ModelViewSet):
    queryset=product.objects.all()
    serializer_class=ProductBysubcategory

    def retrieve(self, request, *args, **kwargs):
        _id=kwargs['pk']
        pro=product.objects.filter(sub_cat=_id)
        serializers=ProductBysubcategory(pro,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
# class ProductDetailView(RetrieveAPIView):
#     queryset = product.objects.all()
#     serializer_class =ProductBysubcategory 
#     lookup_field = 'id' 
        
# fucntion for APIS
class productViewset(ModelViewSet):
    queryset = product.objects.all()
    serializer_class = productserializer

class subcatViewset(ModelViewSet):
    queryset=sub_cat.objects.all()
    serializer_class=subcatserializer


class orderViewset(ModelViewSet):
    queryset=ordernow.objects.all()
    serializer_class=OrderSeriaizer

    def create(self, request, *args, **kwargs):
      
      pro_id=request.data.get("pro_id")
      products=product.objects.get(id=pro_id)
      quantity=request.data.get('quantity',1)
      shipping_adress=request.data.get("shipping_adress")
      user_id=request.data.get("user_id")

      order = ordernow.objects.create(
          product=product.product_name,
          price=product.product_price,
          quantity=quantity,
          shipping_adress=shipping_adress,
          delivery_date = datetime.today().date(),
          user_id=user_id  
      )

      order.save()
      product.stock -= quantity
      product.is_available = product.stock > 0
      product.save()
        
      serializer = OrderSeriaizer(order)
      return Response(serializer.data)



class UserViewset(ModelViewSet):
    queryset= User.objects.all()
    serializer_class=UserSerializer
    permission_classes = (permissions.AllowAny,) 
    # permission_classes=(permissions.AllowAny,)
    def create(self,request,*args,**kwargs):
        data=request.data
        username=data['username']
        first_name=data['first_name']
        last_name=data['last_name']
        email=data['email']
        password=data['password']
        phonenumber=data['phonenumber'] 
        # is_vendor=data.get['is_vendor']
        is_vendor = data.get('is_vendor')

        if User.objects.filter(username=username).exists():
            return Response({'error':"username already exists"},status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        userprofile.objects.create(
            user=user,
            phonenumber=phonenumber,
            is_vendor=is_vendor
        )

        # serializer=self.get_serializer(user,context={'request':request})
        serializer=UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class UserprofileViewset(ModelViewSet):
    queryset=userprofile.objects.all()
    serializer_class=Userprofileserializer


#(Retrieve function)dynamic url api

class SubCategoryByCategoryViewset(ModelViewSet):
    queryset = sub_cat.objects.all()    
    serializer_class = SubCategoryByCategory

    def retrieve(self, request, *args, **kwargs):
        _id = kwargs['pk']
        sub = sub_cat.objects.filter(cat_id = _id)
        serializer=SubCategoryByCategory(sub,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        

class ProductImageviewset(ModelViewSet):
    queryset=ProductImage.objects.all()
    serializer_class=ProductImageSerializer
    def create(self,request,*args,**kwargs):
        product_id=request.data.get('product_id')
        # product=request.data.get('product')

        images=request.FILES.getlist('file')

        uploded_img=[]
        product_detail =product.objects.get(id=product_id)

        # breakpoint()

        for img in images:
            image_obj=ProductImage.objects.create(product_detail=product_detail, image=img)
            image_obj.save()
            uploded_img.append(image_obj)
        breakpoint()
        serializer=ProductImageSerializer(uploded_img,many=True)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class reviewViewset(ModelViewSet):
    queryset=reviews.objects.all()
    serializer_class=reviewserializer

    def create(self, request, *args, **kwargs):
         review = request.data['review']
         rating = request.data['rating']
         product_id = request.data['product_id']
         
         print(review,rating,product_id)
         review = reviews.objects.create(
             product_id = product_id,
             user_id = 14,
             review = review,
             rating = rating
         )
         review.save()
 
         s = reviewserializer(review)
         return Response(s.data,status=status.HTTP_201_CREATED)
    
    

    # def list(self, request, *args, **kwargs):
    #     breakpoint()
    #     print(request)
    #     review = reviews.objects.all()
    #     rvs = reviewserializer(review,many=True)
    #     return Response(rvs.data,status=status.HTTP_200_OK)
    
class CategoryViewSet(ModelViewSet):
    queryset = cat.objects.all()
    serializer_class = CategorySerializer
    def create(self,request,*args,**kwargs):
        cat_name=request.data.get('cat_name')
        cat_pic=request.FILES.get('cat_pic')
        category=cat.objects.create(
            cat_name=cat_name,
            cat_pic=cat_pic,
            user_id=request.user.id
        )
        category.save()

        c=CategorySerializer(category)
        return Response(c.data,status=status.HTTP_201_CREATED)  
def homepage(request):
    category=cat.objects.all()
    return render(request,'index.html',{'cat':category,'user':request.user})
def sub_category(request,id):
    category_instances = cat.objects.get(id=id) 
    sub_category = sub_cat.objects.filter(cat=category_instances)
    return render(request, 'show_sub_cat.html', {'sub_cat': sub_category, 'cat': category_instances})


def createuser(request):
    print(request.POST)
    if request.method == "POST":
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password=request.POST['password']
        email=request.POST['email']
        phonenumber=request.POST['phonenumber']
        is_vendor=request.POST.get('is_vendor')
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("Error:Username already exists please enter another user name")
        
        user=User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()
        profile=userprofile.objects.create(
            user=user,
            phonenumber=phonenumber,
            is_vendor=is_vendor
        )
        profile.save()
        return HttpResponse("user is created susssfully")
    else:
        return render(request,"createuser.html")
def create_cat(request):
    if request.method == "GET":
        return render(request,"category.html")
    else:
        cat_name=request.POST.get('cat_name')
        cat_pic=request.FILES['cat_pic']
        
        category=cat.objects.create(cat_name=cat_name,cat_pic=cat_pic,user=request.user )
        category.save()
        return HttpResponse("your category added sucessfully")
def aboutus(request):
    if request.method=="GET":
        return render(request,'about.html')
def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("Username and password are not valid")
    
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        return render(request, 'login.html' ) 
def userlogout(request):
    logout(request)
    return HttpResponseRedirect("/")
def  add_sub_category(request,id):
    _cat=cat.objects.get(id=id)
    if request.method == "POST":
        sub_cat_name=request.POST['sub_cat_name']
        sub_cat_pic=request.FILES['sub_cat_pic']
        sub_category=sub_cat.objects.create(sub_cat_name=sub_cat_name,sub_cat_pic=sub_cat_pic,cat=_cat)
        sub_category.save()
        return HttpResponse("your category added sussfully")
    return render(request,'sub_cat.html')
def get_profile(request):
    if request.user.is_authenticated:
        try:
            profile_instances=request.user.profile
            is_vendor=profile_instances.is_vendor
        except userprofile.DoesNotExist:
            is_vendor=False
        return render(request,'profile.html',{'user':request.user,'is_vendor':is_vendor})
    else:
        return redirect('/')



def pro_detail(request, id):
    products = product.objects.get(id=id)
    reviews_list = reviews.objects.filter(product=products)
    return render(request, 'product_detail.html',{'product':products,'reviews':reviews_list})

def add_product(request, id):
    _subcat = sub_cat.objects.get(id=id)
    
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        # product_pic = request.FILES.get('product_pic')
        product_dis=request.POST.get('product_dis')
        product_size=request.POST.get('product_size')
        product_color=request.POST.get('product_color')
        product_type=request.POST.get('product_type')
        product_seleve=request.POST.get('product_seleve')
        product_fit=request.POST.get('product_fit')
        packof=request.POST.get('packof')
        fabric=request.POST.get('fabric')
        stock=request.POST.get('stock')



        products = product.objects.create(
            product_name=product_name,
            product_price=product_price,
            product_dis=product_dis,
            product_color=product_color,
            product_size=product_size,
            sub_cat=_subcat,
            user=request.user,
            product_type=product_type,
            product_seleve=product_seleve,
            product_fit=product_fit,
            packof=packof,
            fabric=fabric,
            stock=stock
            )
        
        
        products.save()
        
        # if request.FILES.getlist('images'):
        for image_file in request.FILES.getlist('images'):
            images = ProductImage.objects.create(
                product_detail=products,
                image=image_file)
                # image=request.FILES['images'])
            images.save()

        return HttpResponse("Your product has been added successfully")
    
    
    return render(request, "product.html")
def show_pro(request,id):
    #  sub_category  breakpoint()
     products = product.objects.filter(sub_cat_id = id)
     paginator=Paginator(products,1)
     page_number=request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     return render(request,'show_product.html',{'page_obj':page_obj})


def order_now(request, id):
    if not request.user.is_authenticated:
        return redirect('login') 

    pro = product.objects.get(id=id)
    total_price = 0
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))  # Default to 1 if no quantity is provided
        total_price = pro.product_price * quantity  
        shipping_adress = request.POST.get('shipping_adress')
        payment_method = request.POST.get('payment_method')

        # Get the current stock from the product model
        current_stock = pro.stock

        # Check if the quantity is available in stock
        if current_stock < quantity:
            return HttpResponse(f"Not enough stock available. Only {current_stock} units are in stock.")

        # Update the stock after the order
        new_stock = current_stock - quantity
        pro.stock = new_stock
        pro.save()  # Save the updated stock in the product model

        # Create the order
        order_pro = ordernow.objects.create(
            user=request.user, 
            product=pro,
            price=pro.product_price,
            status="pending",
            shipping_adress=shipping_adress,
            payment_method=payment_method,
            quantity=quantity,
            total_price=total_price, 
            stock=quantity  # Save the quantity ordered, not the stock left
        )
        order_pro.save()

        return HttpResponseRedirect(f"/order_history/{order_pro.id}")
    
    return render(request, 'ordernow.html', {'product': pro})


   
def addbag(request,id):
    products=product.objects.get(id=id)
    qu=request.POST.get('qu')
    date=request.POST.get('date')
    if product.stock==0:
        print("No stock available")
    else:
        print("stock is available")
    bags=bag.objects.create(
        user=request.user,
        product=products,
        qu=qu,
        # date=date
    )
    bags.save()
    return render(request,'add_bag.html',{'product':products})
def canfirm_booking(request,id):
    order = ordernow.objects.get(id=id)
    order.status="canfirmed"
    order.save()
    return HttpResponse("your order booked ")

def order_history(request,id):
    order = ordernow.objects.get(id=id) 
    return render(request, 'canfirmbooking.html' ,{'order':order})

def cancelbooking(request, id):
   order=ordernow.objects.get(id=id)
   order.status="cancelled"    
   order.delete()
   order.save()
   return redirect("/") 
def user_profile(request):
    order=ordernow.objects.filter(user=request.user)
    paginator=Paginator(order,5)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'userprofile.html',{'page_obj':page_obj})


def sreach(request):
    query=request.GET.get('query','')
    if query:
        products=product.objects.filter( product_name__icontains=query) 
    
    else:
        products=product.objects.all()
    return render(request,'search.html',{'products':products,'query':query})


# def review(request, id):
#     pro = get_object_or_404(product, id=id)
#     review = None  # Initialize review and rating to avoid errors
#     rating = None
    

#     if request.method == 'POST':
#         review = request.POST.get('review')
#         rating = request.POST.get('rating')
#         if review and rating:
#             pr = reviews.objects.create(
#                 review=review,
#                 rating=rating,
#                 product=pro,
#                 user=request.user
#             )
#             pr.save()

#     return render(request, 'postget.html', {'product': pro})
# def show_rev(request):
#     r=reviews.objects.all()
#     # r.save()
#     return render(request,'product_detail.html',{'r':r})

def show_bag(request):
    # Logic to display the contents of the bag or show an empty bag if no products are added
    return render(request, 'show_bag.html', {'user': request.user})
def ajax(request):
    return render (request,'newpage.html')
def ajax1(request):
    return render(request,'Postget.html')
def get(request):
    return render(request,'get.html')
def catpost(request):
    return render(request,'categorypost.html')
def productimages(request):
    return render(request,'productget.html')
def product_img(request):
    return render(request,'productpost.html')