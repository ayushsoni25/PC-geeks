from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pic/CustomerProfilePic/', null=True, blank=True)
    address=models.CharField(max_length=50)
    mobile_no=models.CharField(max_length=13,null=False)
    def __str__(self):
        return self.user.first_name
    @property
    def thumbnail_preview(self):
        if self.profile_pic:
            return mark_safe('<img src="/static{}" width="100" height=100 />'.format(self.profile_pic.url) )
        return ""

class Product(models.Model):
    Name=models.CharField(max_length=2000)
    product_pic=models.ImageField(upload_to='product_image/',null=True,blank=True)
    price=models.CharField(max_length=20)
    description=models.CharField(max_length=10000)
    def __str__(self):
        return self.Name
    @property
    def thumbnail_preview(self):
        if self.product_pic:
            return mark_safe('<img src="/static{}" width="100" height=100 />'.format(self.product_pic.url) )
        return ""

class Order(models.Model):
    STATUS=(
    ('Pending','Pending'),
    ('Order Confirmed','Order Confirmed'),
    ('Out Of Delivery','Out Of Delivery'),
    ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('Customer',on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email=models.CharField(max_length=20)
    mobile=models.CharField(max_length=13)
    address=models.CharField(max_length=50)
    order_date=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    def __str__(self):
        return ""
    @property
    def thumbnail_preview(self):
        if self.profile_pic:
            return mark_safe('<img src="/static{}" width="100" height=100 />'.format(self.profile_pic.url) )
        # return ""
class FeedBack(models.Model):
    name=models.CharField(max_length=20)
    feedback=models.CharField(max_length=500)
    email=models.EmailField(max_length=50,default="")
    date=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
    @property
    def thumbnail_preview(self):
        if self.profile_pic:
            return mark_safe('<img src="/static{}" width="100" height=100 />'.format(self.profile_pic.url) )
        return ""
