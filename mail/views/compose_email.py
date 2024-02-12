from django.shortcuts import render, redirect

from mail.forms import EmailComposeForm
from mail.models import Email


def compose_email(request):
    if request.method == 'POST':
        form = EmailComposeForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            # Create the email instance
            email = Email.objects.create(sender=sender, subject=subject, body=body, recipient=recipient)
            return redirect('mail:read', slug=email.slug)
    else:
        form = EmailComposeForm()
    return render(request, 'mailbox/compose.html', {'form': form})
