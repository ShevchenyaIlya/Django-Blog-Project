from django.contrib.auth.models import User

from django.utils import timezone
from mixer.backend.django import mixer
from django.urls import reverse
from users.models import Profile
import pytest
from PIL import Image


@pytest.fixture
def user(request, db):
    return mixer.blend(User, username=request.param)


@pytest.mark.parametrize('user', ['shevchenya'], indirect=True)
def test_profile(user):
    profile = Profile.objects.get(user=user)

    assert profile.verified is False
    assert str(profile) == f"{user.username} Profile"

    img = Image.new('RGB', (400, 400), color='red')
    img.save('/home/shevchenya/PycharmProjects/django_project/media/image.png')
    profile.image = '/home/shevchenya/PycharmProjects/django_project/media/image.png'
    profile.save()
    img = Image.open(profile.image.path)
    assert img.height <= 300
    assert img.width <= 300



