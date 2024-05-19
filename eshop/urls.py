from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('',views.home_view,name='hv'),
    path('home/',views.navbar_view,name='home'),
    path('searching/',views.search_view,name='searchbar'),
    path('product_des/<int:myinid>/',views.product_details,name='product_details'),
    path('signup/',views.customer_signup,name='csign'),
    path('login/',LoginView.as_view(template_name='offview/login.html'),name='clog'),
    path('afterlogin/',views.afterlogin_view,name='afterlogin'),
    path('customer_home/',views.customer_home_view,name='customer_home'),
    path('cart/<int:myinid>', views.add_cart,name='add-to-cart'),
    path('cart/', views.cart_view,name='cart'),
    path('cart-guest/', views.cart_view_guest,name='cartguest'),
    path('remove-from-cart/<int:myinid>/', views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-purchase/',views.customer_purchase_view,name="customer-purchase"),
    path('payment-success/',views.payment_success_view,name='payment-success'),
    path('logout/', LogoutView.as_view(template_name='offview/logout.html'),name='logout'),
    path('my-order/', views.my_order_view,name='my-order'),
    path('send-feedback/', views.send_feedback_view,name='send-feedback'),
    path('send-feedbackguest/', views.send_feedback_view_guest,name='send-feedbackguest'),
    path('contactus', views.contactus_view,name='contactus'),
    path('contactusg/', views.contactusg_view,name='contactusg'),
    path('my-profile/', views.my_profile_view,name='my-profile'),
    path('edit-profile/', views.edit_profile_view,name='edit-profile'),
]
