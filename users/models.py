from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from .managers import CustomUserManager
from PIL import Image


class User(AbstractUser):
    """
    Default custom user model for My Awesome Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Profile(models.Model):
    """
    Model representing user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
