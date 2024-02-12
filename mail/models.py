import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


# Create your models here.


class Email(models.Model):
    """
    Represents an email message.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    attachments = models.FileField('Attachment', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=16, unique=True, default=uuid.uuid4, editable=False, blank=True)
    is_archived = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_recipient = models.BooleanField(default=False)
    is_starred_by_sender = models.BooleanField(default=False)
    is_starred_by_recipient = models.BooleanField(default=False)
    parent_email = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def mark_as_read(self):
        """
        Marks the email as read.
        """
        if not self.is_read:
            self.is_read = True
            self.save()

    def toggle_deleted(self):
        """
        Toggle the deletion status of the email.

        If the email is deleted, it will be restored, and vice versa.
        """
        self.is_deleted_by_sender = not self.is_deleted_by_sender
        self.is_deleted_by_recipient = not self.is_deleted_by_recipient
        self.save()

    def toggle_archive(self):
        """
        Toggle the archive status of the email.

        If the email is archived, it will be unarchived, and vice versa.
        """
        self.is_archived = not self.is_archived
        self.save()

    def toggle_starred(self, user):
        """
        Toggle the archive status of the email.

        If the email is archived, it will be unarchived, and vice versa.
        """
        if user == self.sender:
            self.is_starred_by_sender = not self.is_starred_by_sender
        elif user == self.recipient:
            self.is_starred_by_recipient = not self.is_starred_by_recipient
        self.save()

    def get_absolute_url(self):
        """
        Returns the absolute URL for viewing the email.
        """
        return reverse('read', args=[str(self.slug)])

    def __str__(self):
        """
        Returns a string representation of the email.
        """
        return f"{self.subject} - {self.sender.email}"


class Reply(models.Model):
    """
    Represents a reply to an email.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.ForeignKey('Email', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_replies(cls, email):
        """
        Retrieves replies for a given email.
        """
        return cls.objects.filter(email=email).order_by('timestamp').select_related('sender')

    def get_notification_recipient(self):
        # Determine the recipient based on the sender and email participants
        if self.sender == self.email.sender:
            return self.email.recipient
        elif self.sender == self.email.recipient:
            return self.email.sender
        else:
            # Handle the case where the sender is neither the sender nor the recipient
            return None
