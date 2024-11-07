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

@method_decorator(login_required,name='dispatch')
class reservation_view(View):
    def get(self, request):
        form = ReservationForm()
        return render(request, 'app/reservation_form.html', locals())

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Set the user for the reservation
            reservation = form.save(commit=False)
            reservation.user = request.user  # assuming the user is logged in
            reservation.save()
            messages.success(request, "Congratulations! Table Booked Successfully")
            return redirect('success')  # Change this to your URL name for managing reservations
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/reservation_form.html', {'form': form})

@method_decorator(login_required,name='dispatch')       
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Inavalid Input Data")
        return render(request, 'app/customerregistration.html',locals())

@method_decorator(login_required,name='dispatch')  
class ManageReservationView(View):
    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        return render(request, 'app/managereservation.html', {'reservations': reservations})

@method_decorator(login_required,name='dispatch')
class DeleteReservationView(View):
    def get(self, request, reservation_id):
        # Get the reservation object, or return 404 if not found
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

        # Check if the reservation belongs to the current user
        if reservation.user == request.user:
            # Get the current time and the reservation time
            current_time = timezone.now()
            reservation_datetime = timezone.datetime.combine(reservation.date, reservation.time)

            # Make reservation_datetime timezone-aware
            reservation_datetime = timezone.make_aware(reservation_datetime)

            # Check if the reservation is at least 1 hour away
            if reservation_datetime > current_time + timezone.timedelta(hours=1):
                reservation.delete()
                messages.success(request, "Reservation deleted successfully.")
            else:
                messages.error(request, "You cannot delete a reservation less than 1 hour before the scheduled time.")
        else:
            messages.error(request, "You are not authorized to delete this reservation.")

        return redirect("manage_reservation")  # Redirect back to manage reservations page

base_dir = 'C:\\Users\\SANIYA\\Downloads\\Rospl Project\\food'


# Define the pickle directory
pickle_dir = os.path.join(base_dir, 'pickle')

# Load basic_dict.pkl
basic_dict_path = os.path.join(pickle_dir, 'basic_dict.pkl')
with open(basic_dict_path, 'rb') as file:
    basic_dict_data = pickle.load(file)

# Convert basic_dict_data to a DataFrame
food = pd.DataFrame(basic_dict_data)

# Load similarity1.pkl
similarity1_path = os.path.join(pickle_dir, 'similarity1.pkl')
with open(similarity1_path, 'rb') as file:
    similarity1 = pickle.load(file)

# Load similarity2.pkl
similarity2_path = os.path.join(pickle_dir, 'similarity2.pkl')
with open(similarity2_path, 'rb') as file:
    similarity2 = pickle.load(file)


def menu(request):
    # Retrieve all products from the database
    products = Product.objects.all()
    
    # Create a list to store zipped data
    zipped_data = []
    
    # Iterate over each product and zip its attributes
    for product in products:
        zipped_data.append((product.food_name, product.food_category, product.Image, product.price, product.id))
    
    # Pass the zipped data to the template
    context = {
        'zipped_data': zipped_data,
    }
    
    # Render the template with the data
    return render(request, 'app/menu.html', context)