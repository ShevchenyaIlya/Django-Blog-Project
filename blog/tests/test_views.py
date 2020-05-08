from django.http import Http404
from django.test import RequestFactory, Client, TestCase
from django.utils import timezone
from mixer.backend.django import mixer
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
import pytest

from blog.models import Post, Comment
from blog.views import home, PostListView, UserPostListView, about, PostDetailView, PostCreateView

"""@classmethod
def setUpClass(cls):
    super(TestViews, cls).setUpClass()
    cls.factory = RequestFactory()"""


@pytest.fixture(scope='module')
def factory():
    return RequestFactory()


@pytest.fixture()
def user(request, db):
    return mixer.blend(User, username=request.param)


@pytest.mark.parametrize('user', ['Ilya'], indirect=True)
def test_post_list_view(factory, user):
    path = reverse('blog-home')
    request = factory.get(path)
    request.user = user
    view = PostListView.as_view()
    response = view(request)
    assert response.status_code == 200


@pytest.mark.parametrize('user', ['shevchenya'], indirect=True)
def test_user_post_list_view(factory, user):
    path = reverse('user-posts', kwargs={'username': 'shevchenya'})
    request = factory.get(path)
    request.user = user
    view = UserPostListView.as_view()
    response = view(request, *[], username='shevchenya')
    assert response.status_code == 200


@pytest.mark.parametrize('user', ['Ivan'], indirect=True)
def test_home_view(factory, user):
    path = reverse('blog-home')
    request = factory.get(path)
    request.user = user
    response = home(request)
    assert response.status_code == 200


@pytest.mark.parametrize('user', ['shevchenya'], indirect=True)
def test_about_view(factory, user):
    path = reverse('blog-about')
    request = factory.get(path)
    response = about(request)

    assert response.status_code == 200


class TestFuncViews(TestCase):

    def test_about_view_GET(self):
        client = Client()
        response = client.get(reverse('blog-about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')

    def test_home_view_GET(self):
        client = Client()
        response = client.get(reverse('blog-home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')


class TestPostDetailView(TestCase):
    def setUp(self):
        self.view = PostDetailView()

    def test_attributes(self):
        self.assertEqual(self.view.model, Post)


class TestPostCreateView(TestCase):
    def setUp(self):
        self.view = PostCreateView()

    def test_attributes(self):
        self.assertEqual(self.view.model, Post)
        self.assertEqual(self.view.fields, ['title', 'content'])


@pytest.mark.parametrize('user', ['shevchenya'], indirect=True)
def test_form_validation(factory, user):
    path = reverse('post-create')
    request = factory.get(path)
    request.user = user
    view = PostCreateView.as_view()
    response = view(request)
    assert response.status_code == 200

    request = factory.post(path)
    request.user = AnonymousUser()
    response = view(request)
    assert response.status_code != 200
    assert 'login' in response.url


def test_create_view_form_valid(client, django_user_model):
    path = reverse('post-create')
    user = django_user_model.objects.create_user(username='ilya', password='sheva', email='sheva@gmail.com')
    client.force_login(user)
    response = client.post(path, {'title': 'Hello', 'content': 'World'}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_update_view_form_valid(client, django_user_model):
    user = django_user_model.objects.create_user(username='ilya', password='sheva', email='sheva@gmail.com')
    client.force_login(user)
    post = Post.objects.create(title='Test', author=user, content='Test')
    path = reverse('post-update', kwargs={'pk': post.pk})
    response = client.post(path, {'title': 'Hello', 'content': 'World'}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_delete_view_form_valid(client, django_user_model):
    user = django_user_model.objects.create_user(username='vova', password='vovchick', email='vovan@gmail.com')
    client.force_login(user)
    post = Post.objects.create(title='Test', author=user, content='Test')
    path = reverse('post-delete', kwargs={'pk': post.pk})
    response = client.get(path, follow=True)
    assert response.status_code == 200

    response = client.post(path, follow=True)
    assert response.status_code == 200
