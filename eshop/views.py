from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from . import models,forms
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.
def home_view(request):
    product=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')

    context={'pd':product,'product_count_in_cart':product_count_in_cart}
    return render(request,'offview/index.html/',context)



def navbar_view(request):
    return redirect('hv')


def search_view(request):
    query=request.GET["query"]
    product=models.Product.objects.all().filter(Name__icontains=query)
    context={'pd':product}
    return render(request,"offview/index.html/",context)


def product_details(request,myinid):
    product=models.Product.objects.filter(id=myinid)[0]
    context={'pd':product}
    return render(request,'offview/productdetails.html',context)


def customer_signup(request):
    usereshop=forms.UserEshopPC()
    customereshop=forms.CustomerEshopPC()
    if request.method=="POST":
        usereshop=forms.UserEshopPC(request.POST)
        customereshop=forms.CustomerEshopPC(request.POST,request.FILES)
        if usereshop.is_valid() and customereshop.is_valid():
            user=usereshop.save()
            user.set_password(user.password)
            user.save()
            customer=customereshop.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group=Group.objects.get_or_create(name="CUSTOMER")
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('/login/')
    context={"usereshop":usereshop,"customereshop":customereshop}
    return render(request,"offview/signup.html",context)

def afterlogin_view(request):
    return redirect('customer_home')

@login_required(login_url='clog')
def customer_home_view(request):
    product=models.Product.objects.all()

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'offview/customer_home.html',{'pd':product,'product_count_in_cart':product_count_in_cart})



def add_cart(request,myinid):
    products=models.Product.objects.all()
    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'offview/index.html',{'pd':products,'product_count_in_cart':product_count_in_cart})

    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(myinid)
        else:
            product_ids=product_ids+"|"+str(myinid)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', myinid)
    product=models.Product.objects.get(id=myinid)
    return response


def cart_view(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    product=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            product=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for myin in product:
                total=(int(myin.price)+total)
    return render(request,'offview/cart.html',{'pd':product,'total':total,'product_count_in_cart':product_count_in_cart})


def cart_view_guest(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    product=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            product=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for myin in product:
                total=(int(myin.price)+total)
    return render(request,'offview/cartguest.html',{'pd':product,'total':total,'product_count_in_cart':product_count_in_cart})


def remove_from_cart_view(request,myinid):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(myinid))
        product=models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for myin in product:
            total=(int(myin.price)+total)

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'offview/cart.html',{'pd':product,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response


@login_required(login_url="clog")
def customer_purchase_view(request):
# this is for checking whether product is present in cart or not
# if there is no product in cart we will not show address form
 product_in_cart=False
 if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart=True
    #for counter in cart
 if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
 else:
        product_count_in_cart=0
 AddressForm=forms.AddressForm()
 if request.method=='POST':
        AddressForm=forms.AddressForm(request.POST)
        if AddressForm.is_valid():
            # here we are taking address, email, mobile at time of order placement
            # we are not taking it from customer account table because
            # these thing can be changes
            email=AddressForm.cleaned_data['Email']
            mobile=AddressForm.cleaned_data['Mobile']
            address=AddressForm.cleaned_data['Address']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
            total=0
            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    product=models.Product.objects.all().filter(id__in = product_id_in_cart)
                    for myin in product:
                        total=(int(myin.price)+total)

            response = render(request, 'offview/payment.html',{'total':total})
            response.set_cookie('email',email)
            response.set_cookie('mobile',mobile)
            response.set_cookie('address',address)
            return response
 return render(request,'offview/customer_address.html',{'AddressForm':AddressForm,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})


@login_required(login_url='customerlogin')
def payment_success_view(request):
    # Here we will place order | after successful payment
    # we will fetch customer  mobile, address, Email
    # we will fetch product id from cookies then respective details from db
    # then we will create order objects and store in db
    # after that we will delete cookies because after order placed...cart should be empty
    customer=models.Customer.objects.get(user_id=request.user.id)
    products=None
    email=None
    mobile=None
    address=None
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)
            # Here we get products list that will be ordered by one customer at a time

    # these things can be change so accessing at the time of order...
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']
    # print(products)
    # here we are placing number of orders as much there is a products
    # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
    # there will be lot of redundant data in orders table...but its become more complicated if we normalize it
    for product in products:
        models.Order.objects.get_or_create(customer=customer,product=product,status='Pending',email=email,mobile=mobile,address=address)

    # after order placed cookies should be deleted
    response = render(request,'offview/payment_success.html')
    response.delete_cookie('product_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    return response

@login_required(login_url='clog')
def my_order_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    orders=models.Order.objects.all().filter(customer_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)

    return render(request,'offview/my_order.html',{'data':zip(ordered_products,orders)})

def send_feedback_view(request):
    feedbackForm=forms.FeedBackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedBackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'offview/Feedback_sent.html')
    return render(request, 'offview/send_feedback.html', {'feedbackForm':feedbackForm})



def send_feedback_view_guest(request):
        feedbackForm=forms.FeedBackForm()
        if request.method == 'POST':
            feedbackForm = forms.FeedBackForm(request.POST)
            if feedbackForm.is_valid():
                feedbackForm.save()
                return render(request,'offview/Feedback_sent.html')
        return render(request, 'offview/send_feedbackguest.html', {'feedbackForm':feedbackForm})

@login_required(login_url='clog')
def my_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'offview/myp.html',{'customer':customer})

@login_required(login_url='clog')
def edit_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.UserEshopPC(instance=user)
    customerForm=forms.CustomerEshopPC(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.UserEshopPC(request.POST,instance=user)
        customerForm=forms.CustomerEshopPC(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('/my-profile')
    return render(request,'offview/editprofile.html',context=mydict)



def contactus_view(request):
    return render(request,'offview/contact_us.html')


def contactusg_view(request):
    return render(request,'offview/contact_usg.html')
