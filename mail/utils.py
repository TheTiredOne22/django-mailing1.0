from allauth.core.internal.http import redirect
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Email


def star_email(request, slug):
    email = get_object_or_404(Email, slug=slug)
    if request.user == email.recipients or email.sender:
        email.is_starred = not email.is_starred
        email.save()
    return HttpResponse()


def toggle_starred_email(request, slug):
    """
    View to toggle the starred status of a specific email.

    Toggles the starred status of the email with the given slug if the authenticated user is the sender or recipient.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the email to toggle starred status.

    Returns:
        HttpResponseRedirect: Redirects to the inbox after toggling archive status.
    """
    # Retrieve the email to toggle archive status
    email = get_object_or_404(Email, slug=slug)

    # Check if the authenticated user is the sender or recipient of the email
    if request.user == email.sender or request.user == email.recipient:
        # Toggle the archive status of the email
        email.toggle_starred()

    # Redirect to the inbox after toggling archive status
    return redirect('mail:inbox')


def filter_emails(emails, search_query):
    if search_query:
        return emails.filter(Q(subject__icontains=search_query) |
                             Q(sender__full_name__icontains=search_query))
    else:
        return emails
