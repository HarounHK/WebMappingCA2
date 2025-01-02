from django.contrib.gis.db import models
from django.contrib import admin
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    genres = models.TextField(null=True, blank=True)
    avg_rating = models.FloatField(null=True, blank=True)
    num_ratings = models.IntegerField(null=True, blank=True)
    book_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserBooks(models.Model):
    STATUS_CHOICES = [
        ('TO_READ', 'Want to Read'),
        ('READ', 'Read'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'book', 'status')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.status}"

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.PointField(null=True, blank=True)

    def __str__(self):

        return self.user.username
    
    def set_user_location(user_id, latitude, longitude):
        user = User.objects.get(id=user_id)
        location = Point(longitude, latitude)  

        profile, created = Profile.objects.get_or_create(user=user)
        profile.location = location
        profile.save()

        return profile

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

admin.site.register(Location)

class SavedLocation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
