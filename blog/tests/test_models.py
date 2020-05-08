from mixer.backend.django import mixer
from django.urls import reverse
import pytest


@pytest.fixture
def post(request, db):
    return mixer.blend('blog.Post', title=request.param, pk=100)


@pytest.fixture
def comment(request, db):
    return mixer.blend('blog.Comment', comment_text=request.param)


@pytest.mark.parametrize('post', ['Amazon'], indirect=True)
def test_post(post):
    assert str(post) == 'Amazon'
    assert post.get_absolute_url() == reverse('post-detail', kwargs={'pk': 100})


@pytest.mark.parametrize('comment', ['Test is passed'], indirect=True)
def test_comment(comment):
    assert str(comment) == 'Test is passed'
