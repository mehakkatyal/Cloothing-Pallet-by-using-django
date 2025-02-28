from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from app.models import userprofile,cat,sub_cat,product,ProductImage,ordernow,bag
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from.serializers import *


# fucntion for APIS
class productViewset(ModelViewSet):
    queryset = product.objects.all()
    serializer_class = productserializer
class subcatViewset(ModelViewSet):
    queryset=sub_cat.objects.all()
    serializer_class=subcatserializer
class UserViewset(ModelViewSet):
    queryset= User.objects.all()
    serializer_class=Userserializer

class CategoryViewSet(ModelViewSet):
    queryset = cat.objects.all()
    serializer_class = CategorySerializer






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
    return render(request, 'product_detail.html',{'product':products})

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
    #  sub_category = sub_cat.objects.get(id=id)
     products = product.objects.filter(sub_cat_id = id)
     paginator=Paginator(products,1)
     page_number=request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     return render(request,'show_product.html',{'page_obj':page_obj})

# def order_now(request, id):
#     if not request.user.is_authenticated:
#         return redirect('login') 
#     pro = product.objects.get(id=id)
#     total_price = 0
#     if request.method == "POST":
#         quantity = int(request.POST.get("quantity", 1)) 
#         total_price = pro.product_price * quantity  
#         shipping_adress = request.POST.get('shipping_adress')
#         payment_method = request.POST.get('payment_method')
#         status = "pending" 
#         # stock=request.POST.get('stock')
#         # stock1=quantity-stock
#         stock = request.POST.get('stock')
#         if stock is None:
#             stock = 0
#         else:
#             stock = int(stock)  # Convert stock to integer

#         stock1 = quantity - stock
#         order_pro = ordernow.objects.create(
#             user=request.user, 
#             product=pro,
#             price=pro.product_price,
#             status=status,
#             shipping_adress=shipping_adress,
#             payment_method=payment_method,
#             quantity=quantity,
#             total_price=total_price, 
#             stock=stock1
#         )
#         order_pro.save()
#         return HttpResponseRedirect(f"/order_history/{order_pro.id}")
#     return render(request, 'ordernow.html',{'product': pro})
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
        date=date
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



