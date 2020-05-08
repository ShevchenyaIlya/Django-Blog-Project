from django.urls import reverse, resolve
from users.views import register, profile
from django.contrib.auth import views


class TestUserUrls:

    def test_register_url(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'
        assert resolve(path).func == register

    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'
        assert resolve(path).func.view_class == views.LoginView

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'
        assert resolve(path).func.view_class == views.LogoutView

    def test_password_reset_url(self):
        path = reverse('password_reset')
        value = resolve(path)
        assert value.view_name == 'password_reset'
        assert value.func.view_class == views.PasswordResetView

    def test_profile_url(self):
        path = reverse('profile')
        value = resolve(path)
        assert value.view_name == 'profile'
        assert value.func == profile