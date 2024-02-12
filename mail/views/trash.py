from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from mail.models import Email
from mail.utils import filter_emails


def trash(request):
    # Filter soft-deleted emails for the current user, whether they were the sender or recipient
    emails = Email.objects.filter(
        Q(sender=request.user, is_deleted_by_sender=True) |
        Q(recipient=request.user, is_deleted_by_recipient=True)
    ).order_by('-timestamp')

    # Retrieve search query from GET parameters
    search_query = request.GET.get('q')

    if search_query:
        trashed_emails = filter_emails(emails, search_query)
    else:
        trashed_emails = emails

    paginator = Paginator(trashed_emails, 10)  # Show 10 emails per page
    page_number = request.GET.get('page')
    trashed_emails = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'mailbox/partials/search/trash-search-results.html',
                      {'trashed_emails': trashed_emails})
    else:
        # Render the archive page with the retrieved emails
        return render(request, 'mailbox/trash.html', {'trashed_emails': trashed_emails})


# def delete_email(request, slug):
#     if request.method == 'POST':
#         email = get_object_or_404(Email, slug=slug)
#         if request.user == email.sender:
#             email.is_deleted_by_sender = True
#         elif request.user == email.recipient:
#             email.is_deleted_by_recipient = True
#         email.save()
#         messages.success(request, 'Email deleted successfully')
#     return redirect('mail:inbox')
#
#
# def bulk_delete(request):
#     if request.method == 'POST':
#         email_ids = request.POST.getlist('email_ids')
#         emails = Email.objects.filter(id__in=email_ids)
#         for email in emails:
#             if request.user == email.sender:
#                 email.is_deleted_by_sender = True
#             elif request.user == email.recipient:
#                 email.is_deleted_by_recipient = True
#             email.save()
#         messages.success(request, 'Emails deleted successfully.')
#     return redirect('mail:inbox')


#

def delete_email(request, slug):
    """
    View to toggle the deletion status of a specific email.

    Toggles the deletion status of the email with the given slug if the authenticated user is the sender or recipient.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the email to toggle deletion status.

    Returns:
        HttpResponseRedirect: Redirects to the inbox after toggling deletion status.
    """
    # Retrieve the email to toggle deletion status
    email = get_object_or_404(Email, slug=slug)

    # Check if the authenticated user is the sender or recipient of the email
    if request.user == email.sender or request.user == email.recipient:
        # Toggle the deletion status of the email
        email.toggle_deleted()

    # Redirect to the trash page after toggling deletion status
    return redirect('mail:trash')


def bulk_delete(request):
    if request.method == 'POST':
        email_ids = request.POST.getlist('email_ids[]')
        emails = Email.objects.filter(id__in=email_ids)
        for email in emails:
            email.toggle_deleted()

    if request.htmx:
        return render(request, 'mailbox/partials/search/trash-search-results.html')
    else:
        return redirect('mail:trash')


def permanently_delete_email(request, slug):
    # Retrieve the email instance or return a 404 response if not found
    email = get_object_or_404(Email, id=slug)

    # Ensure the email is marked as deleted before permanently deleting

    # Permanently delete the email
    email.delete()
    return redirect('mail:trash')


def permanent_bulk_delete(request):
    if request.method == 'POST':
        email_ids = request.POST.getlist('email_ids[]')
        emails = Email.objects.filter(id__in=email_ids)
        for email in emails:
            email.delete()

    return redirect('mail:trash')
