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
from .views import feedback, reservation_view, ManageReservationView,  DeleteReservationView, delete_order
from django.contrib.auth import views as auth_view
from .forms import LoginForm,  MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.home),
    path('product-detail/<int:pk>/',
         views.ProductDetail.as_view(), name='product-detail'),
    path("about/", views.aboutview.as_view(), name="about"),
    path("home/", views.homeview.as_view(), name="home"),
    path("contact/", views.contactview.as_view(), name="contact"),
    path("shop/", views.shopview.as_view(), name="shop"),
    path('blog/', views.blog, name='blog'),
    path('fullblog/<slug:slug>/', views.fullblog, name='fullblog'),
    path('createblog/', views.create_blog, name='create_blog'),
    path('feedback/', feedback, name='feedback'),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.show_cart, name="showcart"),
    path("wishlist/", views.wishlistview.as_view(), name="wishlist"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('search/', views.search, name="search"),
    path('address/', views.address, name="address"),
    path('updateAddress/<int:pk>',
         views.updateAddress.as_view(), name="updateAddress"),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart, name='minus-cart'),
    path('removecart/', views.remove_cart, name='removecart'),

    
    #Reservation
    path('reservation/', views.reservation_view.as_view(), name='reservation'),
    path('managereservation/', ManageReservationView.as_view(),
         name='manage_reservation'),
    path('delete-reservation/<int:reservation_id>/',
         DeleteReservationView.as_view(), name='delete_reservation'),

    #Payment
    path('checkout/', views.checkout.as_view(), name="checkout"),
    path('paymentdone/', views.payment_done, name="paymentdone"),
    path('orders/', views.orders, name="orders"),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),




     #new urls
     path('menu/', views.menu, name='menu'),
     path('recommend/', views.recommended_ui, name='recommend'),
     path('recommend_foods/', views.recommend_foods, name='recommend_foods'),


    #login authentication
    path('register/', views.CustomerRegistrationView.as_view(), name='registration'),
    path('login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name="login"),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'),name="passwordchange"),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name="passwordchangedone"),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'),name="logout"),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# admin.site.site_header = "Foodie"
# admin.site.site_title = "Foodie"
# admin.site.site_index_title = "Welcome to Foodie"

