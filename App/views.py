from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from .models import Hotel_details
from django.http import HttpResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from django.core.mail import send_mail
from django.conf import settings
import os

# Custom login view to redirect already logged-in users to home
class CustomLoginView(LoginView):
    redirect_authenticated_user = True

# Home view, protected by login_required decorator
@login_required
def home(request):
    return render(request, "home.html")

# Signup view to create a new user
def SignupView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# View to display hotel list with city filter and sorting
def hotels(request):
    cities = Hotel_details.objects.values('city').distinct()
    return render(request, 'hotels.html', {'cities': cities})

# Booking view to display booking page for a specific hotel
def booking(request, hotel_id):
    hotel = get_object_or_404(Hotel_details, id=hotel_id)

    # Mock data for special offers and advertisements
    special_offers = [
        {"description": "10% off on weekend stays", "discount": 10},
        {"description": "Free breakfast for family bookings", "discount": 0},
    ]
    
    advertisements = [
        {"title": "Exclusive Spa Offers", "image_url": "/static/images/spa_offer.jpg"},
        {"title": "50% off on Pool Access", "image_url": "/static/images/pool_offer.jpg"},
    ]

    # Chart data
    chart_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
        "values": [100, 200, 150, 300, 250],
    }

    payment_methods = ["Credit Card", "Debit Card", "UPI", "Net Banking"]

    context = {
        'hotel': hotel,
        'special_offers': special_offers,
        'advertisements': advertisements,
        'chart_data': chart_data,
        'payment_methods': payment_methods,
    }

    return render(request, 'booking.html', context)

def blog(request):
    return render(request, 'blog.html')

def contact_us(request):
    return render(request, 'contact_us.html')

# Hotel list view with sorting based on user selection
def hotel_list(request):
    city = request.GET.get('city', None)
    checkin = request.GET.get('checkin', None)
    checkout = request.GET.get('checkout', None)
    guests = request.GET.get('guests', None)
    rooms = request.GET.get('rooms', None)
    sort_by = request.GET.get('sort', 'popular')

    hotels = Hotel_details.objects.all()

    if city:
        hotels = hotels.filter(city__iexact=city)

    if rooms:
        hotels = hotels.filter(room_count__gte=rooms)  # Assuming 'room_count' exists

    if sort_by == 'low-to-high':
        hotels = hotels.order_by('price')
    elif sort_by == 'high-to-low':
        hotels = hotels.order_by('-price')
    elif sort_by == 'popular':
        hotels = hotels.order_by('-rating')

    return render(request, 'hotel_list.html', {'hotels': hotels})

# Hotel detail view for a specific hotel
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel_details, id=hotel_id)
    return render(request, 'hotel_detail.html', {'hotel': hotel})
def booking_redirect(request):
    # Redirect to the first hotel or a default hotel if no hotel_id is provided
    default_hotel = Hotel_details.objects.first()  # Choose any hotel as the default or implement your own logic
    if default_hotel:
        return redirect('booking', hotel_id=default_hotel.id)
    else:
        return redirect('hotels') 
def credit_card_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        amount = request.POST.get('amount')

        # Process payment logic here, e.g., using a payment gateway API.

        return HttpResponse("Payment successful!")  # Example response, you can redirect or display a message

    return render(request, 'credit_card_payment.html')  
def send_email(to_email, subject, message):
    message = Mail(
        from_email='youremail@example.com',
        to_emails=to_email,
        subject=subject,
        plain_text_content=message
    )
    try:
        sg = SendGridAPIClient('SENDGRID_API_KEY')
        sg.send(message)
    except Exception as e:
        print(e.message)
def send_sms(to_phone, message):
    account_sid = 'TWILIO_ACCOUNT_SID'
    auth_token = 'TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_='+1234567890',  # Your Twilio phone number
        to=to_phone
    )   
def contact_us(request):
    return render(request, 'App/contact_us.html')
def contact_us(request):
    print("Template directories:", os.environ.get('DJANGO_TEMPLATE_DIRS'))  # Prints the template dirs
    return render(request, 'contact_us.html')
def submit_contact_form(request):
    if request.method == 'POST':
       
        return redirect('thank_you')  
    else:
       
        return render(request, 'contact_us.html')
def contact_us(request):
    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Prepare the email
        subject = f"Message from {name}"
        message_body = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send email
        send_mail(
            subject,
            message_body,
            email,  # From email (this will be the email entered by the user)
            ['admin@example.com'],  # Admin email (replace with your email)
            fail_silently=False,
        )

        # Redirect to thank you page
        return redirect('thank_you')
    
    return render(request, 'contact_us.html')

def thank_you(request):
    return render(request, 'thank_you.html')     