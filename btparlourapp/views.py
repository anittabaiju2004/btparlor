from urllib import request
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'Index.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import tbl_register

# Register View
def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        # Check if the email is already in use
        if tbl_register.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return redirect('register')
        
        # Save the user registration in the database without hashing the password
        new_user = tbl_register(name=name, email=email, password=password, address=address, phone_number=phone_number)
        new_user.save()
        messages.success(request, "User registered successfully!")
        return redirect('login')
    
    return render(request, 'register.html')

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import tbl_register, Admin
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import tbl_register, Admin
from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from django.http import HttpResponse
from .models import tbl_register, Admin

def login(request):
    if request.method == "POST":
        password = request.POST['password']  # Password field
        email = request.POST['email']  # Email field

        # Check for a regular user in tbl_register (user type "user")
        var = tbl_register.objects.filter(password=password, email=email)
        
        # Check for a photographer in Admin table
        var2 = Admin.objects.filter(email=email, password=password)

        # If user is found in tbl_register
        if var:
            for x in var:
                if x.status == "blocked":
                    # If user status is blocked, deny login
                    txt = """<script>alert("Your account has been blocked."); window.location='/';</script>"""
                    return HttpResponse(txt)
                request.session['id'] = x.id  # Store user ID in session
            return render(request, 'user/user_index.html')  # Redirect to user dashboard

        # If photographer is found in Admin table
        elif var2:
            for x in var2:
                request.session['id'] = x.id  # Store admin ID in session
            return render(request, 'admin/admin_index.html')  # Redirect to admin dashboard

        # If no matching user or photographer is found, show an alert
        else:
            txt = """<script>alert("Invalid user credentials...."); window.location='/';</script>"""
            return HttpResponse(txt)  # Return an alert if login fails

    else:
        return render(request, "login.html")  # If not POST, render the login page

def logout(reqeust):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return render(request,"login.html")


def user_index(request):
    return render(request,'user/user_index.html')
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import tbl_register

def user_profile(request):
    # Check if user is logged in
    user_id = request.session.get('id')  # Assuming you are storing user ID in session
    if not user_id:
        return redirect('login')  # Redirect to the login page if not authenticated

    # Retrieve the user details from the tbl_register model
    user = get_object_or_404(tbl_register, id=user_id)

    return render(request, 'user/user_profile.html', {'user': user})
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import tbl_register

def edit_profile(request):
    user_id = request.session.get('id')
    if user_id is None:
        return redirect('login')  # Redirect to login if user is not authenticated

    user = get_object_or_404(tbl_register, id=user_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Corrected to 'password'
        address = request.POST.get('address')  # Corrected to 'address'
        phone_number = request.POST.get('phone_number')  # Corrected to 'phone_number'

        # Update the user information
        user.name = name
        user.email = email
        user.password = password  # Ensure you handle password hashing if needed
        user.address = address
        user.phone_number = phone_number
        user.save()  # Save the updated user information

        return redirect('user_profile')  # Redirect to the user profile page after saving

    return render(request, 'user/edit_profile.html', {'user': user})


from .models import Admin

def admin_index(request):
    return render(request, 'admin/admin_index.html')

# views.py
from django.shortcuts import render
# from django.contrib.auth.models import User
from .models import *

def view_users(request):
    users = tbl_register.objects.all()  # Fetch all users from the database
    return render(request, 'admin/view_user.html', {'users': users})


# btparlourapp/views.py

from django.shortcuts import get_object_or_404, redirect
from .models import tbl_register  # Make sure to import your User model

def approve_user(request, user_id):
    user = get_object_or_404(tbl_register, id=user_id)
    user.status = 'approved'
    user.save()
    return redirect('view_users')  # Redirect back to the user list page

def block_user(request, user_id):
    user = get_object_or_404(tbl_register, id=user_id)
    user.status = 'blocked'
    user.save()
    return redirect('view_users')  # Redirect back to the user list page


from django.shortcuts import render, redirect
from .models import Feedback, tbl_register

from django.shortcuts import render, redirect
from .models import Feedback, tbl_register
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Feedback, tbl_register
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Feedback, tbl_register  # Adjust import as needed

def send_feedback(request):
    if request.method == "POST":
        user_id = request.session.get('id')
        message = request.POST.get("message")
        rating = request.POST.get("rating")

        if not user_id:
            return HttpResponse("<script>alert('User not logged in!'); window.location='/login/';</script>")

        if message and rating:
            try:
                user = tbl_register.objects.get(id=user_id)
                Feedback.objects.create(user=user, message=message, rating=int(rating))
                return redirect("feedback_success")
            except tbl_register.DoesNotExist:
                return HttpResponse("<script>alert('User does not exist!'); window.location='/login/';</script>")

    feedbacks = Feedback.objects.select_related('user').order_by('-created_at')  # Get all feedbacks, latest first
    return render(request, "user/send_feedback.html", {
        "feedbacks": feedbacks
    })




def feedback_success(request):
    return render(request, "user/feedback_success.html")


from django.shortcuts import render
from .models import Feedback

def view_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')  # Show newest first
    return render(request, 'admin/view_feedback.html', {'feedback_list': feedback_list})


from django.shortcuts import render, redirect
from .models import BeautyService
from django.shortcuts import render, redirect
from .models import BeautyService

def add_beauty_service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        duration = request.POST.get("duration")
        image = request.FILES.get("image")

        if name and description and price and duration and image:
            BeautyService.objects.create(
                name=name,
                description=description,
                price=price,
                duration=duration,
                image=image
            )
            return redirect("view_beauty_services")  # Redirect to the service list page

    return render(request, "admin/add_beauty_service.html")

from django.shortcuts import render
from .models import BeautyService

def view_beauty_services(request):
    services = BeautyService.objects.all()  # Fetch all beauty services
    return render(request, 'admin/view_beauty_services.html', {'services': services})


from django.shortcuts import render, get_object_or_404, redirect
from .models import BeautyService

def edit_service(request, service_id):
    service = get_object_or_404(BeautyService, id=service_id)
    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.duration = request.POST.get('duration')
        if 'image' in request.FILES:
            service.image = request.FILES['image']
        service.save()
        return redirect('view_beauty_services')
    return render(request, 'admin/edit_service.html', {'service': service})


def delete_service(request, service_id):
    service = get_object_or_404(BeautyService, id=service_id)
    service.delete()
    return redirect('view_beauty_services')

from django.shortcuts import render
from .models import BeautyService

def user_view_beauty_services(request):
    services = BeautyService.objects.all()
    return render(request, 'user/user_view_beauty_services.html', {'services': services})
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import BeautyService, Booking, tbl_register, Payment  # Import the Payment model
from django.http import HttpResponse
from datetime import datetime, date, time

def book_service(request, service_id):
    service = get_object_or_404(BeautyService, id=service_id)
    user_id = request.session.get('id')

    if user_id is None:
        return HttpResponse("User not logged in. Please log in to book a service.")

    user = get_object_or_404(tbl_register, id=user_id)

    if request.method == 'POST':
        booking_date_str = request.POST.get('booking_date')
        booking_time_str = request.POST.get('booking_time')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
        booking_time = datetime.strptime(booking_time_str, "%H:%M").time()

        # Validate date (not in the past)
        if booking_date < date.today():
            return HttpResponse("Booking date cannot be in the past.")

        # Validate time (between 10 AM and 10 PM)
        if not (time(10, 0) <= booking_time <= time(22, 0)):
            return HttpResponse("Booking time must be between 10:00 AM and 10:00 PM.")

        # Create booking
        booking = Booking(
            user=user,
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
            email=email,
            name=name,
            phone_number=phone_number
        )
        booking.save()

        return redirect('payment_page', booking_id=booking.id)

    return render(request, 'user/book_service.html', {'service': service, 'user': user})

# views.# views.py
from decimal import Decimal
# views.py
from .models import Notification  # Import the Notification model
from decimal import Decimal

from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Payment, Notification

def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    amount = booking.service.price * Decimal('0.50')

    if request.method == 'POST':
        cardholder_name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number')  # Already trimmed to last 4 by JS
        cvv = request.POST.get('cvv')
        expiry_date = request.POST.get('expiry_date')

        # Extra server-side validation (optional)
        if not card_number or len(card_number) != 4 or not card_number.isdigit():
            return render(request, 'user/payment_page.html', {
                'booking': booking, 'amount': amount,
                'error': 'Invalid card number (must be last 4 digits).'
            })
        if not cvv or len(cvv) != 3 or not cvv.isdigit():
            return render(request, 'user/payment_page.html', {
                'booking': booking, 'amount': amount,
                'error': 'Invalid CVV.'
            })
        # Expiry date format check (MM/YY, not past)
        from datetime import datetime
        try:
            mm, yy = expiry_date.split('/')
            exp_month = int(mm)
            exp_year = int('20' + yy)
            expire = datetime(exp_year, exp_month, 1)
            today = datetime.now().replace(day=1)
            if expire < today:
                raise ValueError
        except Exception:
            return render(request, 'user/payment_page.html', {
                'booking': booking, 'amount': amount,
                'error': 'Invalid expiry date.'
            })

        payment = Payment(
            user=booking.user,
            booking=booking,
            cardholder_name=cardholder_name,
            card_number=card_number,
            cvv=cvv,
            expiry_date=expiry_date,
            amount=amount
        )
        payment.save()

        booking.payment_status = True
        booking.save()

        Notification.objects.create(
            user=booking.user,
            message=f"A new booking has arrived for {booking.service.name} on {booking.booking_date} at {booking.booking_time}."
        )

        request.session['booking_id'] = booking.id
        return redirect('booking_success')

    return render(request, 'user/payment_page.html', {'booking': booking, 'amount': amount})
def booking_success(request):
    # Get the booking ID from the session
    booking_id = request.session.get('booking_id')

    if not booking_id:
        return redirect('user_index')  # Redirect to user index or an error page if no booking ID is found

    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, 'user/booking_success.html', {'booking': booking})



# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, tbl_register

def user_bookings(request):
    user_id = request.session.get('id')  # Assuming you store the user ID in the session
    if user_id is None:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Retrieve the user object
    user = get_object_or_404(tbl_register, id=user_id)

    # Get all bookings for the user
    bookings = Booking.objects.filter(user=user)

    return render(request, 'user/user_bookings.html', {'bookings': bookings})



# views.pyfrom django.shortcuts import render, get_object_or_404
from .models import Booking, Payment

def payment_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = get_object_or_404(Payment, booking=booking)
    return render(request, 'user/payment_details.html', {'booking': booking, 'payment': payment})


def all_bookings(request):
    bookings = Booking.objects.all()  # Retrieve all bookings
    return render(request, 'admin/all_bookings.html', {'bookings': bookings})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking, Notification, tbl_register  # Import the Notification model

def cancel_booking(request, booking_id):
    # Get the user ID from the session
    user_id = request.session.get('id')  # Assuming you store the user ID in the session

    # Check if the user ID is present in the session
    if user_id is None:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Retrieve the booking
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if the user is the owner of the booking
    if booking.user.id != user_id:
        return redirect('user_bookings')  # Redirect if the user is not authorized

    # Create a notification for the user indicating the booking has been canceled
    Notification.objects.create(user=booking.user, message=f"A booking for {booking.service.name} on {booking.booking_date} at {booking.booking_time} has been canceled.")

    booking.delete()  # Delete the booking
    return redirect('user_bookings')  # Redirect to the bookings page with a success message



def send_notification(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            AdminNotification.objects.create(message=message)
            messages.success(request, "Notification sent successfully!")
        else:
            messages.error(request, "Message cannot be empty.")
    return redirect('notifications')



from django.shortcuts import render, redirect, get_object_or_404
from .models import AdminNotification, Notification, tbl_register
from django.views.decorators.csrf import csrf_exempt

def admin_notifications_view(request):
    # For sending a notification
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Save admin notification
            admin_notif = AdminNotification.objects.create(message=message)
            # Optionally, create a Notification for each user:
            for user in tbl_register.objects.all():
                Notification.objects.create(user=user, message=message)
        return redirect('admin_notifications')

    sent_notifications = AdminNotification.objects.all().order_by('-created_at')
    return render(request, 'admin/notifications.html', {
        'sent_notifications': sent_notifications,
    })

# Optionally, allow admin to delete notifications
@csrf_exempt
def delete_admin_notification(request, notif_id):
    if request.method == 'POST':
        notif = get_object_or_404(AdminNotification, id=notif_id)
        notif.delete()
        # Also delete from user's notifications
        Notification.objects.filter(message=notif.message, created_at=notif.created_at).delete()
    return redirect('admin_notifications')

# User's view for received notifications
def notifications(request):
    user_id = request.session.get('id')
    if user_id is None:
        return redirect('login')
    user = get_object_or_404(tbl_register, id=user_id)
    received_notifications = Notification.objects.filter(user=user).order_by('-created_at')
    return render(request, 'admin/received_notifications.html', {
        'received_notifications': received_notifications,
    })




from django.shortcuts import render
from .models import AdminNotification

def user_notifications(request):
    notifications = AdminNotification.objects.all().order_by('-created_at')
    return render(request, 'user/user_notifications.html', {'notifications': notifications})