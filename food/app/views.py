from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
import razorpay
from .models import Customer, Product, Reservation, Feedback, Cart, Payment, OrderPlaced, Blog # Replace with your actual model
from . forms import ReservationForm, CustomerProfileForm,  BlogForm  # Ensure you have a form defined
from decimal import Decimal
from django.db.models import Count, Q, F
from django.contrib import messages
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import pickle
import os
import pandas as pd
import numpy as np
from datetime import datetime
from django.utils import timezone
import hmac
import hashlib

#import stripe

from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@login_required
def home(request):
    return render(request,"app/home.html")

@method_decorator(login_required,name='dispatch')    
class aboutview(View):
    def get(self,request):
        return render(request,"app/about.html")
    
@method_decorator(login_required,name='dispatch')    
class wishlistview(View):
    def get(self,request):
        return render(request,"app/wishlist.html")

@method_decorator(login_required,name='dispatch')     
class contactview(View):
    def get(self,request):
        return render(request,"app/contact.html")

@method_decorator(login_required,name='dispatch')    
class homeview(View):
    def get(self,request):
        return render(request,"app/home.html")
    
@method_decorator(login_required,name='dispatch')    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            village = form.cleaned_data['village']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']

            reg = Customer(user=user,name=name,village=village,city=city,mobile=mobile,state=state,pincode=pincode)
            reg.save()
            messages.success(request, "Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profile.html',locals())
    
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.village = form.cleaned_data['village']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.pincode = form.cleaned_data['pincode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

@method_decorator(login_required,name='dispatch')
class shopview(View):
    def get(self,request):
        return render(request,"app/shop.html")

@login_required  
def feedback(request):
    return render(request, 'app/feedback.html')

@login_required
def search(request):
    query = request.GET.get('search')
    # Check if the query is a valid decimal for price
    try:
        price = Decimal(query)
        products = Product.objects.filter(
            Q(food_name__icontains=query) |
            Q(food_category__icontains=query) |
            Q(sub_category__icontains=query) |
            Q(price__lte=query)  # Exact match for price
        )
    except:
        # If the query is not a valid decimal, filter without price
        products = Product.objects.filter(
            Q(food_name__icontains=query) |
            Q(food_category__icontains=query) |
            Q(sub_category__icontains=query)
        )

    return render(request, "app/search.html", {'products': products, 'query': query})

@login_required
def feedback(request):
    if request.method=="POST":
        feedback=Feedback()
        name=request.POST.get('name')
        email=request.POST.get('email')
        comment=request.POST.get('comment')
        feedback.name=name
        feedback.email=email
        feedback.comment=comment
        feedback.save()
        # return HttpResponse("<center><h1>THANKS FOR YOUR FEEDBACK</h1><center>")
        return redirect("/")
    return render(request, 'app/feedback.html',locals())



@login_required   
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Handle file upload
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.username  # Automatically set author as the logged-in user
            blog.save()
            return redirect('blog')  # Redirect to the blog list page
    else:
        form = BlogForm()
    return render(request, 'app/create_blog.html', {'form': form})

@login_required
def blog(request):
    blogs = Blog.objects.all().order_by('-date')   # Get all blog posts
    return render(request, 'app/blog.html', {'blogs':blogs})

@login_required
def fullblog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)  # Fetch the specific blog post by slug
    return render(request, 'app/fullblog.html', {'blog': blog}) 
