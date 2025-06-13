from django.db import models

# Create your models here.
from django.db import models
from django.db import models

class tbl_register(models.Model):
    APPROVAL_CHOICES = [
        ('approved', 'Approved'),
        ('blocked', 'Blocked'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    status = models.CharField(
        max_length=10,
        choices=APPROVAL_CHOICES,
        default='approved',
    )

    def __str__(self):
        return self.name


class Admin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
            
    def __str__(self):
        return self.email

        # btparlourapp/models.py

from django.db import models
from django.db import models

class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Ratings from 1 to 5

    user = models.ForeignKey('tbl_register', on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)  # Default 5-star rating
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.name} - {self.rating} stars"



from django.db import models

class BeautyService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")  # New field for duration
    image = models.ImageField(upload_to='beauty_services/')  # Stores images in media/beauty_services/

# models.py
from django.db import models

class Booking(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    service = models.ForeignKey(BeautyService, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    email = models.EmailField()
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.service.name} on {self.booking_date} at {self.booking_time}"


# models.py
from django.db import models
class Payment(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=4)  # Only last 4 digits stored
    cvv = models.CharField(max_length=3)
    expiry_date = models.CharField(max_length=5)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Payment of {self.amount} for {self.booking}"


    

# models.py
from django.db import models
# from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(tbl_register, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.created_at}"
    


from django.db import models

class AdminNotification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)