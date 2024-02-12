from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView

from mail.models import Email
from mail.utils import filter_emails


@login_required
def inbox(request):
    """
    View function for displaying the received emails of the logged-in user.
    """
    # Retrieve received emails for the current user, excluding archived ones
    emails = Email.objects.filter(recipient=request.user, is_archived=False,
                                  is_deleted_by_recipient=False).select_related(
        'sender').prefetch_related('replies').order_by(
        '-timestamp')

    # Retrieve search query from GET parameters
    search_query = request.GET.get('q')

    # Apply search filters if a query is present
    if search_query:
        inbox_mail = filter_emails(emails, search_query)
    else:
        inbox_mail = emails

    # Pagination
    paginator = Paginator(inbox_mail, 10)  # Show 10 emails per page
    page_number = request.GET.get('page')
    inbox_mail = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'mailbox/partials/search/inbox-search-results.html', {'inbox_mail': inbox_mail})
    else:
        return render(request, 'mailbox/index.html', {'inbox_mail': inbox_mail})


class SearchMixin(object):

    def get_queryset(self):
        # fetch the queryset from the parent's get_queryset
        queryset = super(SearchMixin, self).get_queryset()

        # get the q GET parameter
        q = self.request.GET('q')
        if q:
            # return a filtered queryset
            return queryset.filter(subject__icontains=q)
        # no q is specified so we return the queryset
        return queryset


class InboxView(LoginRequiredMixin, SearchMixin, ListView):
    model = Email
    Paginate_by = 10
    context_object_name = 'inbox'
    template_name = 'mailbox/index.html'

    def get_queryset(self):
        # Retrieve received emails for the current user, excluding archived ones
        return Email.objects.filter(
            recipient=self.request.user,
            is_archived=False,
            is_deleted_by_recipient=False
        ).select_related('sender').prefetch_related('replies').order_by('-timestamp')
