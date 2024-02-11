from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from PIL import Image


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Model representing user profile information.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='profile_images',
        blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """
        String representation of the Profile instance.
        """
        return self.user.email

    def save(self, *args, **kwargs):
        """
        Override the save method to resize the avatar image if it exceeds 300x300 pixels.
        """
        super().save(*args, **kwargs)

        # Open the avatar image
        img = Image.open(self.avatar.path)

        # Check if the image dimensions exceed 300x300 pixels
        if img.height > 300 or img.width > 300:
            # Resize the image to fit within 300x300 pixels
            output_size = (300, 300)
            img.thumbnail(output_size)
            # Save the resized image
            img.save(self.avatar.path)
