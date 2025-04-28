
from django.contrib import admin
from django.urls import path, include
from app.views import *
from rest_framework import routers  # Import routers here
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenVerifyView
router = routers.DefaultRouter()  # Now you can use routers here

# Register your viewsets with the router
router.register(r'product', productViewset,basename='product')
router.register(r'sub_cat', subcatViewset,basename='sub_cat')
router.register(r'user', UserViewset)
router.register('category',CategoryViewSet)
router.register('review',reviewViewset)
router.register('productimage',ProductImageviewset)
# Retrieve function url
router.register('subcategory_by_category',SubCategoryByCategoryViewset,basename='subcategory_by_category')

urlpatterns = [
    # genric view set url
    path('api/sub_cat_by_cat/<int:id>',CatBySubCat.as_view()),
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
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('review/<int:id>/',review),
    path('bag/', show_bag, name='show_bag'),
    path('ajax',ajax),
    path('ajax1',ajax1),
    path('get',get),
    path('catpost',catpost),
    path('productget',productimages),
    path('product_img',product_img),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
