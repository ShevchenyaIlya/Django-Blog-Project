import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer
from django.contrib import messages

from users.form import UserRegisterForm
from users.models import Profile
from users.tokens import account_activation_token
from users.views import register, activate, profile, send


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture()
def user(request, db):
    return mixer.blend(User, username=request.param)


@pytest.mark.parametrize('user', ['Abed'], indirect=True)
def test_profile_view(factory, user):
    path = reverse('profile')
    request = factory.get(path)
    request.user = user
    response = profile(request)
    assert response.status_code == 200

    request = factory.post(path)
    request.user = user
    response = profile(request)
    assert response.status_code == 200


def test_register_view(client, django_user_model):
    path = reverse('register')
    response = client.get(path)
    assert response.status_code == 200

    response = client.post(path, {'username': 'ilya', 'first_name': 'ilya', 'last_name': 'shevchenya', 'email': 'shevchenya.i@gmail.com', 'password1': 'asdfghjkiu78', 'password2': 'asdfghjkiu78'}, follow=True)
    assert response.status_code == 200


def test_profile_view_form_validation(client, django_user_model):
    user = django_user_model.objects.create_user(username='ilya', password='sheva', email='sheva@gmail.com')
    client.force_login(user)
    path = reverse('profile')
    user_profile = Profile.objects.get(user=user)
    response = client.post(path, {'username': 'Ilya', 'email': 'sheva@gmail.com', 'first_name': 'Ilya', 'last_name': 'Shevchenya', 'image': user_profile.image, 'date_of_birth': user_profile.date_of_birth}, follow=True)
    assert response.status_code == 200


def test_activate_view(client, django_user_model):
    path = reverse('activate', kwargs={'uidb64': 1, 'token': 1})
    response = client.post(path, follow=True)
    assert response.status_code == 200

    user = django_user_model.objects.create_user(username='ilya', password='sheva', email='sheva@gmail.com')
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    client.force_login(user)
    response = client.post(path, follow=True)
    assert response.status_code == 200


def test_send_form(client, django_user_model):
    superuser = django_user_model.objects.create_superuser(username='ilya', password='sheva', email='shevchenya.i@gmail.com')
    user = django_user_model.objects.create_user(username='vova', password='netyparolya', email='shevchenya.i@gmail.com')
    client.force_login(superuser)
    path = reverse('admin_email_message', kwargs={'user_id': Profile.objects.get(user=user).pk})
    response = client.get(path, follow=True)
    assert response.status_code == 200