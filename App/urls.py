from django.urls import path, include
from django.shortcuts import redirect  # Import redirect
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', lambda request: redirect('login'), name='root'),  # Redirect root URL to login
    path('home/', views.home, name='home'),
   path('signup/', views.SignupView, name='signup'),
path('accounts/signup/', views.SignupView, name='account_signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # Includes the default auth views
    path('hotels/', views.hotels, name='hotels'),
    path('booking/', views.booking, name='booking'),  # General booking page
    path('booking/<int:hotel_id>/', views.booking, name='booking'),  # Specific hotel booking page
    path('blog/', views.blog, name='blog'),
   path('contact-us/', views.contact_us, name='contact_us'),
    path('hotel_list/', views.hotel_list, name='hotel_list'),
    path('hotel_detail/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('credit-card-payment/', views.credit_card_payment, name='credit_card_payment'),
    path('submit-contact-form/', views.submit_contact_form, name='submit_contact_form'), 
     path('contact-us/', views.contact_us, name='contact_us'),  # URL for contact page
    path('submit-contact/', views.submit_contact_form, name='submit_contact_form'),  # URL for form submission
    path('thank-you/', views.thank_you, name='thank_you'),
   
]
