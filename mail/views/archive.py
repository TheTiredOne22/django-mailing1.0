from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from mail.models import Email
from mail.utils import filter_emails


@login_required()
def archive(request):
    """
    View to display archived emails for the authenticated user.

    Retrieves emails with is_archived=True for the current user and renders them in 'mailbox/archive.html'.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered archive emails page.
    """
    # Filter archived emails for the current user, whether they were the sender or recipient
    emails = Email.objects.filter(
        Q(sender=request.user, is_archived=True) |
        Q(recipient=request.user, is_archived=True)
    ).order_by('-timestamp')

    # Retrieve search query from GET parameters
    search_query = request.GET.get('q')

    if search_query:
        archived_emails = filter_emails(emails, search_query)
    else:
        archived_emails = emails

    paginator = Paginator(archived_emails, 10)  # Show 10 emails per page
    page_number = request.GET.get('page')
    archived_emails = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'mailbox/partials/search/archive-search-results.html',
                      {'archived_emails': archived_emails})
    else:
        # Render the archive page with the retrieved emails
        return render(request, 'mailbox/archive.html', {'archived_emails': archived_emails})


def toggle_archive_email(request, slug):
    """
    View to toggle the archive status of a specific email.

    Toggles the archive status of the email with the given slug if the authenticated user is the sender or recipient.

    Args:
        request (HttpRequest): The request object.
        slug (str): The slug of the email to toggle archive status.

    Returns:
        HttpResponseRedirect: Redirects to the inbox after toggling archive status.
    """
    # Retrieve the email to toggle archive status
    email = get_object_or_404(Email, slug=slug)

    # Check if the authenticated user is the sender or recipient of the email
    if request.user == email.sender or request.user == email.recipient:
        # Toggle the archive status of the email
        email.toggle_archive()

    # Redirect to the inbox after toggling archive status
    return redirect('mail:inbox')


def bulk_archive(request):
    """
    View to bulk archive selected emails.

    Archives multiple emails based on the POST request data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponseRedirect: Redirects to the inbox after bulk archiving selected emails.
    """
    if request.method == 'POST':
        # Retrieve the list of email IDs to be archived from the POST data
        email_ids = request.POST.getlist('email_ids[]')
        emails = Email.objects.filter(id__in=email_ids)
        for email in emails:
            email.toggle_archive()

    # Redirect to the archive after bulk archiving selected emails
    return redirect('mail:archive')
