from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from . import views
from .views import feedback
from django.contrib.auth import views as auth_view
from .forms import LoginForm,  MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.home),
    
    path("about/", views.aboutview.as_view(), name="about"),
    path("home/", views.homeview.as_view(), name="home"),
    path("contact/", views.contactview.as_view(), name="contact"),
    path("shop/", views.shopview.as_view(), name="shop"),
    path('blog/', views.blog, name='blog'),
    path('fullblog/<slug:slug>/', views.fullblog, name='fullblog'),
    path('createblog/', views.create_blog, name='create_blog'),
    path('feedback/', feedback, name='feedback'),
    # Ensure this points to your success view
    path("wishlist/", views.wishlistview.as_view(), name="wishlist"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('search/', views.search, name="search"),
    path('address/', views.address, name="address"),
    path('updateAddress/<int:pk>',
         views.updateAddress.as_view(), name="updateAddress"),
    
    #Payment



     #new urls

    #login authentication
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# admin.site.site_header = "Foodie"
# admin.site.site_title = "Foodie"
# admin.site.site_index_title = "Welcome to Foodie"

