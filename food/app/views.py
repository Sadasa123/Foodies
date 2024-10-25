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
def recommend_by_time():
    now = datetime.now()
    current_time = now.time()

    if datetime.strptime('06:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('10:59:59', '%H:%M:%S').time():
        return recommend_breakfast()
    elif datetime.strptime('11:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('15:59:59', '%H:%M:%S').time():
        return recommend_main_course()
    elif datetime.strptime('16:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('20:59:59', '%H:%M:%S').time():
        return recommend_soup()
    elif datetime.strptime('21:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('23:59:59', '%H:%M:%S').time():
        return recommend_main_course()
    else:
        return [{"food_name": "No recommendations for the current time.", "food_category": "","Image":""}]

@login_required
# Define functions to recommend items for different meal times
def recommend_breakfast():
    # Filter breakfast items
    breakfast_items = Product.objects.filter(food_category='breakfast')
    if breakfast_items.exists():
        # Return recommended breakfast items
        return breakfast_items.values('food_name', 'food_category', 'Image','pk')
    else:
        return [{"food_name": "No breakfast items available.", "food_category": "", "Image": "","pk":""}]

@login_required
def recommend_main_course():
    # Filter main course items
    main_course_items = Product.objects.filter(food_category='main course')
    if main_course_items.exists():
        # Return recommended main course items
        return main_course_items.values('food_name', 'food_category', 'Image','pk')
    else:
        return [{"food_name": "No main course items available.", "food_category": "", "Image": "","pk":""}]

@login_required
def recommend_soup():
    # Filter soup items
    soup_items = Product.objects.filter(sub_category='snack')
    if soup_items.exists():
        # Return recommended soup items
        return soup_items.values('food_name', 'food_category', 'Image','pk')
    else:
        return [{"food_name": "No soup items available.", "food_category": "", "Image": "","pk":""}]

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
class fullblogview(View):
    def get(self,request):
        return render(request,"app/fullblog.html")
    
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

@method_decorator(login_required,name='dispatch')
class shopview(View):
    def get(self,request):
        return render(request,"app/shop.html")

@login_required  
def feedback(request):
    return render(request, 'app/feedback.html')

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

@login_required
def success_view(request):
    return render(request, 'app/success.html')

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

@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
     def get(self, request, pk):
        try:
            # Fetch the product from the database using the provided primary key (pk)
            product = Product.objects.get(id=pk)
            
            # Get recommendations for the current product
            recommendations = recommend(product.food_name)
            
            # Get same category recommendations for the current product
            same_category_recommendations = same_recommend1(product.food_name)

            context = {
                'product': product,
                #'wishlist': wishlist,
                'recommendations': recommendations,
                'same_category_recommendations': same_category_recommendations,
            }
            return render(request, 'app/productdetail.html', context)
        except Product.DoesNotExist:
            # Handle the case where the product with the given primary key doesn't exist
            return HttpResponseNotFound("The requested product does not exist.")

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

@login_required   
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id=product_id)
    
    # Check if the product is already in the cart for the current user
    existing_cart_item = Cart.objects.filter(user=user, product=product).first()
    if existing_cart_item:
        # If the product already exists in the cart, increase the quantity by 1
        existing_cart_item.quantity = F('quantity') + 1
        existing_cart_item.save()
        # messages.success(request, "Quantity updated successfully.")
    else:
        # If the product is not in the cart, add it to the cart with quantity 1
        Cart.objects.create(user=user, product=product)
        # messages.success(request, "Product added to cart successfully.")
    
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    total_amount = 0
    for cart_item in cart_items:
        value = cart_item.quantity * cart_item.product.price
        total_amount += value    
    return render(request, 'app/addtocart.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=int(prod_id))
        cart_item = get_object_or_404(Cart, product=product, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # Use get_object_or_404 to retrieve the cart item
        cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)
        # Delete the cart item
        cart_item.delete()

        # Recalculate the amount and total amount after removing the item
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.price for p in cart)
        totalamount = amount 

        # Prepare data to send back in the JSON response
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@method_decorator(login_required,name='dispatch')   
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value=p.quantity * p.product.price
            famount = famount + value
        totalamount = famount 
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount" :razoramount, "currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html',locals())

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    
    # Log received parameters for debugging
    print(f"Received payment details: order_id={order_id}, payment_id={payment_id}, cust_id={cust_id}")

    # Signature Verification
    signature = request.GET.get('razorpay_signature')
    generated_signature = hmac.new(
        bytes(settings.RAZOR_KEY_SECRET, 'utf-8'),
        msg=(order_id + "|" + payment_id).encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    if generated_signature == signature:
        try:
            # Retrieve payment record
            payment = Payment.objects.get(razorpay_order_id=order_id)

            # Update payment status and payment ID
            payment.paid = True
            payment.razorpay_payment_id = payment_id
            payment.save()

            # Get customer information
            customer = Customer.objects.get(id=cust_id)
            user = request.user

            # Save order details
            cart_items = Cart.objects.filter(user=user)
            for item in cart_items:
                OrderPlaced.objects.create(
                    user=user,
                    customer=customer,
                    product=item.product,
                    quantity=item.quantity,
                    payment=payment
                )
                item.delete()  # Remove item from cart after placing the order

            print("Payment processed successfully, orders placed in the database.")
            return redirect("orders")  # Redirect to orders page on success
        except Payment.DoesNotExist:
            print(f"No payment found with order_id: {order_id}")
            return redirect("checkout")  # Handle case where payment record does not exist
        except Customer.DoesNotExist:
            print(f"No customer found with id: {cust_id}")
            return redirect("checkout")  # Handle case where customer record does not exist
    else:
        print("Signature verification failed.")
        # Handle verification failure
        return redirect("checkout")


@login_required
def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())

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


#base_dir = 'C:\\Users\\SANIYA\\Downloads\\Rospl-Project\\food'

base_dir = 'C:\\Users\\SANIYA\\Downloads\\rospl\\food'


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

@login_required
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

@login_required
def recommended_ui(request):
    return render(request, 'app/recommend.html')

@login_required
def recommend_foods(request):
    if request.method == 'POST':
        # Get the user input from the form
        user_input = request.POST.get('user_input')

        # Recommendation code
        try:
            food_obj = Product.objects.get(food_name=user_input)
            food_index = food_obj.id  # Assuming the IDs are sequential starting from 1
            distances = similarity1[food_index]
            foods_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

            recommendations = []
            for i in foods_list:
                recommended_food = Product.objects.get(pk=i[0] + 1)  # Assuming primary keys are sequential starting from 1
                recommendations.append({
                    "pk": recommended_food.pk,  # Add the primary key here
                    "food_name": recommended_food.food_name,
                    "image_title": recommended_food.Image,
                    "food_category": recommended_food.food_category,
                    "price": recommended_food.price
                })

            same_category_recommendations = get_same_category_foods(user_input)

            return render(request, 'app/recommend.html', {
                'recommendations': recommendations,
                'same_category_recommendations': same_category_recommendations,
                'user_input': user_input
            })
        except Product.DoesNotExist:
            return HttpResponseNotFound("The requested item is currently not available.")

@login_required
def get_same_category_foods(user_input):
    try:
        food_obj = Product.objects.get(food_name=user_input)
        sub_category = food_obj.sub_category
        same_category_foods = Product.objects.filter(sub_category=sub_category).exclude(food_name=user_input)[:9]

        same_category_recommendations = []
        for recommended_food in same_category_foods:
            same_category_recommendations.append({
                "pk": recommended_food.pk,  # Add the primary key here
                "food_name": recommended_food.food_name,
                "image_title": recommended_food.Image,
                "sub_category": recommended_food.sub_category,
                "price": recommended_food.price
            })

        return same_category_recommendations
    except Product.DoesNotExist:
        return []

@login_required
def recommend(food):
    try:
        product = Product.objects.get(food_name=food)
        food_index = product.id - 1
        distances = similarity1[food_index]
        foods_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

        recommendations = []
        for i in foods_list:
            similar_product = Product.objects.get(pk=i[0] + 1)
            recommendations.append({
                "pk": similar_product.pk,
                "food_name": similar_product.food_name,
                "image_title": similar_product.Image,
                "food_category": similar_product.food_category,
                "price": similar_product.price,
            })

        return recommendations
    except Product.DoesNotExist:
        return []

@login_required
def same_recommend1(food):
    try:
        product = Product.objects.get(food_name=food)
        # food_index = product.id - 1
        sub_category = product.sub_category
        same_category_foods = Product.objects.filter(sub_category=sub_category).exclude(food_name=food)[:6]

        recommendations = []
        for recommended_food in same_category_foods:
            recommendations.append({
                "pk": recommended_food.pk,
                "food_name": recommended_food.food_name,
                "image_title": recommended_food.Image,
                "sub_category": recommended_food.sub_category,
                "price": recommended_food.price,
            })

        return recommendations
    except Product.DoesNotExist:
        return []