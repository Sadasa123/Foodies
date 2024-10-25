from django.contrib import admin
from . models import Product, Customer, Reservation, Feedback, Cart, Blog, Payment,OrderPlaced
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'ProductId', 'price', 'food_name', 'food_category', 'sub_category', 'Image')

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'village', 'city', 'mobile', 'pincode', 'state')
    search_fields = ('name', 'village', 'city', 'mobile', 'pincode', 'state')

@admin.register(Reservation)
class ReservationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time', 'guests')
    search_fields = ('name', 'email', 'date', 'time', 'guests')
    list_filter = ('date', 'time', 'guests')

@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display=['name', 'email', 'comment']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.food_name)
                           
                           
@admin.register(Blog)                           
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'message', 'title')  # Fields to display in the list view
    search_fields = ('name', 'message')  # Fields to search in admin
    list_filter = ('date',)  # Filter by date

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customers','products','quantity','ordered_date','status','payments']

    def customers(self,obj):
        link=reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def products(self,obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.food_name)  # Change 'title' to 'food_name'
    
    def payments(self,obj):
        link = reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>',link,obj.payment.razorpay_payment_id)

    def customers(self,obj):
        link=reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def products(self,obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.food_name)  # Change 'title' to 'food_name'
    
    def payments(self,obj):
        link = reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>',link,obj.payment.razorpay_payment_id)