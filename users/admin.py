import datetime
import os
from multiprocessing import Process, Queue, Pool

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_encode

from .models import Profile
from .tokens import account_activation_token

admin.site.site_header = 'Admin Page'


def send(current_user):
    user = current_user.user
    # messages.success(request, f'Success! Email message has been sanded for user: {user},'
    #                          f' email: {user.email}, user id: {user.id}')
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    message = render_to_string('users/acc_active_email.html', {
        'user': user,
        'time': datetime.datetime.now(),
        'domain': 'http://localhost:8000',
        'uid': uid,
        'token': token,
    })
    send_mail("Confirm your registration", "", settings.EMAIL_HOST_USER,
              [user.email], fail_silently=True, html_message=message)


class UserAdmin(admin.ModelAdmin):
    fields = (('user', 'image'), 'verified')
    list_display = ['user', 'image', 'verified', 'date_of_birth', 'id', 'send_email_button']
    list_filter = ['user', ]
    actions = ['send_email']

    def send_email_button(self, obj):
        return format_html('<a class="btn" href="/send/{}/">Send</a>', obj.id)

    send_email_button.allow_tags = True

    def send_email(self, request, queryset):
        if queryset:
            """procs = []
            for current_user in queryset:
                proc = Process(target=send, args=(current_user, ))
                proc.start()
                procs.append(proc)

            for proc in procs:
                proc.join()"""
            recipients = [user for user in queryset]
            pool = Pool(processes=5)
            pool.map_async(send, recipients)

    send_email.short_description = "Send validate email"


admin.site.register(Profile, UserAdmin)


