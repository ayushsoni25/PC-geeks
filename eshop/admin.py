from django.contrib import admin
from .models import Customer,Product,Order,FeedBack
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=('user','mobile_no','address','thumbnail_preview',)

    def thumbnail_preview(self,obj):
        return obj.thumbnail_preview
    thumbnail_preview.short_description='Profile_Pic'
    thumbnail_preview.allow_tags=True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('Name','price','thumbnail_preview',)
    list_editable=['price']
    def thumbnail_preview(self,obj):
        return obj.thumbnail_preview
    thumbnail_preview.short_description='Product_Pic'
    thumbnail_preview.allow_tags=True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('customer','product','email','address','mobile','status','order_date',)
    list_editable=['status']

@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display=('name','feedback','date',)
