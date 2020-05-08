from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
import datetime
import logging
from django.contrib.auth.models import User
from .models import Profile
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('users', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_activate = True
        someone = Profile.objects.get(user=user)
        someone.verified = True
        someone.save()
        user.save()
        messages.success(request, f'Thank you for your email confirmation. Now you can login your account.')
        return redirect('/')
    else:
        messages.success(request, f'Activation link is invalid!')
        return redirect('login')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            logger.debug(u_form, p_form)
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


def send(request, user_id):
    if user_id is not None:
        try:
            user = Profile.objects.get(id=user_id).user
            messages.success(request, f'Success! Email message has been sanded for user: {user},'
                                      f' email: {user.email}, user id: {user_id}')
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            current_site = get_current_site(request)
            template = env.get_template('users/acc_active_email.html')
            activate_url = f"http://{ current_site }/{uid}/{token}/"
            message = template.render(user=user, time=datetime.datetime.now(), activate_url=activate_url)
            send_mail("Confirm your registration", "", settings.EMAIL_HOST_USER,
                      [user.email], fail_silently=True, html_message=message)
        except (TypeError, ValueError, IndexError, IndentationError):
            messages.error(request, f'Fail with sending email message for user profile id - {user_id}')

    return redirect('/admin/users/profile/')

