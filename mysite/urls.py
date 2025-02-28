# """mysite URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path
# from app.views import *
# from django.conf import settings
# from django.conf.urls.static import static
# # from rest_framework import routers
# router = routers.DefaultRouter()
# from django.urls import path, include
# from rest_framework import routers, serializers
# router = routers.DefaultRouter()


# router.register(r'product',productViewset)
# router.register(r'sub_cat',subcatViewset)
# router.register(r'user',userViewset)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('createuser',createuser),
#     path("",homepage),
#     path("createpage",create_cat),
#     path("about",aboutus),
#     path("login",userlogin),
#     path("logout",userlogout),
#     path('sub_cat/<int:id>/',add_sub_category),
#     path('show_sub/<int:id>/', sub_category, name="sub_category"), 
#     # path("addproduct/<int:id>/",add_product)
#     path("addproduct/<int:id>/", add_product),
#     # path("show_product/<int:id>/",show_product),
#      path('show_pro/<int:id>/',show_pro),
#     path('pro_detail/<int:id>/',pro_detail),
#     path('order_now/<int:id>/',order_now),
#     path('bag/<int:id>/',bag),
#     path('booking/<int:id>/',canfirm_booking),
#     path('order_history/<int:id>/',order_history),
#     path('cancel/<int:id>/',cancelbooking),
#     path('userprofile/',user_profile),
#     path('search',sreach),
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))


#     # path('booking/<int:id>/', canfirm_booking, name='booking')

    
    


# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from app.views import *
from rest_framework import routers  # Import routers here
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()  # Now you can use routers here

# Register your viewsets with the router
router.register(r'product', productViewset,basename='product')
router.register(r'sub_cat', subcatViewset,basename='sub_cat')
router.register(r'user', UserViewset)
router.register('category',CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createuser', createuser),
    path("", homepage),
    path("createpage", create_cat),
    path("about", aboutus),
    path("login", userlogin),
    path("logout", userlogout),
    path('sub_cat/<int:id>/', add_sub_category),
    path('show_sub/<int:id>/', sub_category, name="sub_category"),
    path("addproduct/<int:id>/", add_product),
    path('show_pro/<int:id>/', show_pro),
    path('pro_detail/<int:id>/', pro_detail),
    path('order_now/<int:id>/', order_now),
    path('bag/<int:id>/', addbag),
    path('booking/<int:id>/', canfirm_booking),
    path('order_history/<int:id>/', order_history),
    path('cancel/<int:id>/', cancelbooking),
    path('userprofile/', user_profile),
    path('search', sreach),
    path('api/', include(router.urls)),  # Include router URLs
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
