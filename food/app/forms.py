from django import forms
from .models import Reservation 
from . models import Customer, Blog
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'date', 'time', 'guests', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name','style': 'font-size: 18px; height: 35px;' }),
            'email': forms.EmailInput(attrs={ 'class': 'form-control', 'placeholder': 'Your Email','style': 'font-size: 18px; height: 35px;'}),
            'date': forms.DateInput(attrs={ 'class': 'form-control',  'type': 'date', 'placeholder': 'Reservation Date','style': 'font-size: 12px; height: 35px;'}),
            'time': forms.TimeInput(attrs={  'class': 'form-control', 'type': 'time', 'placeholder': 'Reservation Time','style': 'font-size: 12px; height: 35px;'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Number of Guests','style': ' height: 35px;'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Any Special Requests', 'rows': 4 ,'style': 'font-size: 12px;'}),
        }


class CustomerProfileForm(forms.ModelForm):
    mobile = forms.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{0,10}$', message='Mobile number must be 10 digits or less')],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'font-size: 18px; height: 35px;',
            'maxlength': '10'  # Limit input to 10 digits
        })
    )

    pincode = forms.CharField(
        max_length=6,
        validators=[RegexValidator(regex=r'^\d{6}$', message='Pincode must be exactly 6 digits')],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'font-size: 15px; height: 35px;',
            'maxlength': '6'  # Limit input to 6 digits
        })
    )
    
    class Meta:
        model = Customer
        fields=['name','village','city','mobile','state','pincode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder': 'Your Name','style': 'font-size: 18px; height: 35px;'}),
            'village':forms.TextInput(attrs={'class':'form-control','style': 'font-size: 18px; height: 35px;'}),
            'city':forms.TextInput(attrs={'class':'form-control','style': 'font-size: 18px; height: 35px;'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control','style': 'font-size: 15px; height: 35px;'}),
            'state':forms.Select(attrs={'class':'form-control','style': 'font-size: 12px; height: 35px;'}),
            'pincode':forms.NumberInput(attrs={'class':'form-control','style': 'font-size: 15px; height: 35px;'}),
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password' , widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password' , widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password' , widget=forms.PasswordInput(attrs={'autofocus':'True', 'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password' , widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password' , widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password' , widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password' , widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'title', 'message', 'image']  # Include the fields you want

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # Check if the image is not empty
        if not image:
            raise ValidationError("This field is required.")

        # Validate file extension
        valid_extensions = ['.png', '.jpg', '.jpeg']
        if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError("Only PNG, JPG, and JPEG images are allowed.")

        return image


