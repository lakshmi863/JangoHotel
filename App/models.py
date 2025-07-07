from django.db import models

class Hotel_details(models.Model):
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotel_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    room_type = models.CharField(max_length=100)
    guest_capacity = models.IntegerField(default=1)  # Add this field to your model
    room_count = models.IntegerField()  # Add room count if applicable

    def __str__(self):
        return self.name

class SpecialOffer(models.Model):
    hotel = models.ForeignKey(Hotel_details, on_delete=models.CASCADE)  # Reference to Hotel_details
    description = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    image_url = models.URLField()
