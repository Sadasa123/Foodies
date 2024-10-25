from django.db import models
from django.contrib.auth.models import User
import pickle
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

# class YourModel(models.Model):
#     # Define your fields here
#     name = models.CharField(max_length=100)
CATEGORY_CHOICES=(
    ('BR','beverage '),
    ('BF','breakfast'),
    ('DT','dessert'),
    ('MC','main course'),
    ('SP','soup'),
    ('CH','chapati'),
)

# Create your models here.
STATE_CHOICES = (
    ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Daman and Diu','Daman and Diu'),
    ('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Mizoram','Mizoram'),
    ('Meghalaya','Meghalaya'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
)

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    ProductId = models.CharField(max_length=20)
    food_name = models.CharField(max_length=100)
    #food_category = models.CharField(choices=CATEGORY_CHOICES, max_length=100)
    food_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Image = models.CharField(max_length=255)

    def __str__(self):
        return self.food_name


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Temporarily allow null values
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="You must have at least 1 guest."),
            MaxValueValidator(6, message="The maximum number of guests is 6.")  # Adjust as needed
        ]
    )
    message = models.TextField(blank=True,)
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
    ], default='Pending')


    def clean(self):
        # Ensure the reservation date is not in the past
        if self.date < timezone.now().date():
            raise ValidationError("The reservation date cannot be in the past.")

        # Ensure the time is during business hours (e.g., 9 AM to 10 PM)
        # if not (timezone.datetime(2024, 1, 1, 9, 0) <= timezone.datetime.combine(timezone.now(), self.time) <= timezone.datetime(2024, 1, 1, 22, 0)):
        #     raise ValidationError("Reservations can only be made between 9:00 AM and 10:00 PM.")

    def __str__(self):
        message_part = f" Message: {self.message}" if self.message else ""
        return f"{self.name} - {self.date} at {self.time.strftime('%I:%M %p')} for {self.guests} guest(s){message_part}"
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    village = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    mobile = models.IntegerField(default=0,help_text = "Please enter 10 digits valid Number")
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    comment=models.TextField()
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
       
    @property
    def total_cost(self):
        return self.quantity * self.product.price
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)


# Payment
class Payment(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    customer =  models.ForeignKey(Customer,on_delete=models.CASCADE)
    product =  models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status =  models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.price

class Blog(models.Model):
    name = models.CharField(max_length=100)  # User's name
    date = models.DateField(auto_now_add=True)  # Automatically set the date
    slug = models.SlugField(unique=True, blank=True, null=True)  
    title = models.CharField(max_length=255, default='Sample')
    message = models.TextField()  # Blog message
    image = models.ImageField(upload_to='blog_images/')
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug if it doesn't exist
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Image upload field

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title