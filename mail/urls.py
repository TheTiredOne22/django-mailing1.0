from django.urls import path

from .views import inbox, sent, archive, starred, toggle_archive_email, read_email, trash, \
    delete_email, \
    bulk_delete, compose_email, \
    delete_reply, toggle_starred_email, bulk_archive, permanent_bulk_delete, permanently_delete_email

app_name = 'mail'

urlpatterns = [
    # Mailbox views
    path('', inbox, name='inbox'),
    path('compose/', compose_email, name='compose'),
    path('sent/', sent, name='sent'),
    path('starred/', starred, name='starred'),
    path('archive/', archive, name='archive'),
    path('read/<slug:slug>/', read_email, name='read'),
    path('trash/', trash, name='trash'),

    # Delete reply
    path('delete-reply/<int:reply_id>/', delete_reply, name='delete_reply'),

    # Soft delete emails
    path('delete/<slug:slug>/', delete_email, name='delete_email'),
    path('bulk-delete/', bulk_delete, name='bulk_delete'),

    # Permanently delete emails
    path('permanent-delete/<slug:slug>/', permanently_delete_email, name='permanently_delete_email'),
    path('permanent-bulk-delete/', permanent_bulk_delete, name='permanent_bulk_delete'),

    # Archive emails
    path('archive-email/<slug:slug>/', toggle_archive_email, name='archive_email'),
    path('bulk-archive/', bulk_archive, name='bulk_archive'),

    # Utility views
    path('star-emails/<slug:slug>/', toggle_starred_email, name='star_email')
]
