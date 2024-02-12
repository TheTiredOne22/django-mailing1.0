from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mail.models import Email
from mail.utils import filter_emails


@login_required()
def draft(request):
    emails = Email.objects.filter(sender=request.user, is_draft=True)
    search_query = request.GET.get('q')
    draft_mail = filter_emails(emails, search_query)
    return render(request, 'mailbox/draft.html', {'draft_mail': draft_mail})
