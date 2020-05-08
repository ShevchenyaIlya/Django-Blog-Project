from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import datetime
from django.contrib.sites.shortcuts import get_current_site


def create_profile(sender, created=False, **kwargs):
    user = kwargs["instance"]
    if created:
        profile = Profile(user=user)
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        # current_site = get_current_site(sender.request)
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'time': datetime.datetime.now(),
            'domain': "localhost:8000",
            'uid': uid,
            'token': token,
        })
        # message = "http://localhost:8000/activate/" + str(uid) + "/" + str(token)
        send_mail("Confirm your registration", "", settings.EMAIL_HOST_USER,
                  [user.email], fail_silently=True, html_message=message)
        profile.save()


post_save.connect(create_profile, sender=User)

