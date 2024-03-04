
from django.contrib.auth.models import AbstractUser
from django.db import models

from django_countries.fields import CountryField
from django.contrib.auth.models import BaseUserManager
from PIL import Image


class CustomUser(AbstractUser):
    country = CountryField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True)
    user_type = models.CharField(max_length=50, choices=[(
        'Admin', 'Admin'), ('Job Provider', 'Job Provider'), ('Job Seeker', 'Job Seeker')], default='admin')
    profile_img = models.ImageField(
        default='profiles/profile.png', upload_to='customprofile/')

    class Meta:
        db_table = 'Users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    @property
    def is_job_provider(self):
        return self.user_type == 'Job Provider'

class Jobseeker(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_img = models.ImageField(
        default='profiles/profile.png', upload_to='profiles/')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'jobseeker'

    def __str__(self):
        return self.username.email


class Company(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    description = models.TextField()
    image = models.ImageField(
        default='profiles/profile.png', upload_to='company_images/', blank=True, null=True)

    class Meta:
        db_table = 'Company'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Open the image using Pillow
        img = Image.open(self.image.path)

        # Resize the image to 80x80
        img.thumbnail((80, 80))

        # Save the resized image
        img.save(self.image.path)


class JobProvider(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company = models.OneToOneField(
        Company, on_delete=models.CASCADE, null=True, blank=True)
    # Other job provider-related fields

    class Meta:
        db_table = 'JobProvider'
        verbose_name = 'JobProvider'
        verbose_name_plural = 'JobProviders'

    def __str__(self):
        return self.user.username
