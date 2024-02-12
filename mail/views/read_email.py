from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from mail.forms import EmailReplyForm
from mail.models import Email, Reply
# from notifications.models import Notification


@login_required()
def read_email(request, slug):
    """
    Display details of a specific email and handle email replies.

    Parameters:
    - `request`: The HTTP request object.
    - `slug`: The unique identifier for the email.

    Returns:
    - If the request method is GET, renders the 'read.html' template with email details and replies.
    - If the request method is POST and the reply form is valid, adds a new reply and redirects to the same email view.
    """
    email = get_object_or_404(Email, slug=slug)

    # Mark email as read if the authenticated user is the recipient
    if request.user == email.recipient:
        email.mark_as_read()

        notification = Notification.objects.filter(user=request.user, related_email=email).first()
        if notification:
            notification.mark_as_read()

        # Mark reply notifications as read when a user opens a reply
    unread_reply_notifications = Notification.objects.filter(
        user=request.user,
        notification_type=Notification.NotificationType.REPLY,
        related_email=email,
        is_read=False
    )

    for notification in unread_reply_notifications:
        notification.mark_as_read()

    # Retrieve replies and order them by timestamp
    replies = Reply.get_replies(email)

    # Handle the reply form
    form = handle_form(request, email)

    context = {'email': email, 'replies': replies, 'form': form}
    return render(request, 'mailbox/read.html', context)


def handle_form(request, email):
    """
    Handle the email reply form.

    Parameters:
    - `request`: The HTTP request object.
    - `email`: The email object for which the reply form is being handled.

    Returns:
    - If the request method is POST and the form is valid, adds a new reply and redirects to the same email view.
    - If the request method is GET or the form is not valid, returns a new instance of the reply form.
    """
    if request.method == 'POST':
        form = EmailReplyForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.sender = request.user
            new_reply.email = email
            new_reply.save()
            return redirect('mail:read', slug=email.slug)
    else:
        form = EmailReplyForm()
    return form


def delete_reply(request, reply_id):
    """
    Delete a specific reply associated with an email.

    Parameters:
    - `request`: The HTTP request object.
    - `reply_id`: The unique identifier for the reply to be deleted.

    Returns:
    - If the authenticated user is the sender, deletes the reply and redirects to the same email view with a success message.
    - If the authenticated user is not the sender, displays an error message and redirects to the same email view.
    """
    reply = get_object_or_404(Reply, id=reply_id)
    slug = reply.email.slug

    if request.user == reply.sender:
        reply.delete()
        messages.success(request, 'Reply deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this reply.')

    return redirect('mail:read', slug=slug)
