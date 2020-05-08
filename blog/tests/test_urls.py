from django.urls import reverse, resolve
from blog.views import PostDetailView, UserPostListView, PostListView, PostUpdateView, PostDeleteView, PostCreateView, about

class TestUrls:

    def test_post_detail_url(self):
        path = reverse('post-detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'post-detail'
        assert resolve(path).func.view_class == PostDetailView

    def test_post_update_url(self):
        path = reverse('post-update', kwargs={'pk': 10})
        assert resolve(path).view_name == 'post-update'
        assert resolve(path).func.view_class == PostUpdateView


    def test_post_delete_url(self):
        path = reverse('post-delete', kwargs={'pk': 4})
        assert resolve(path).view_name == 'post-delete'
        assert resolve(path).func.view_class == PostDeleteView
        assert resolve(path).kwargs == {'pk': 4}


    def test_post_create_url(self):
        path = reverse('post-create')
        assert resolve(path).view_name == 'post-create'
        assert resolve(path).func.view_class == PostCreateView


    def test_blog_about_url(self):
        path = reverse('blog-about')
        assert resolve(path).view_name == 'blog-about'
        assert resolve(path).func == about


    def test_user_posts_url(self):
        path = reverse('user-posts', kwargs={'username': 'shevchenya'})
        assert resolve(path).view_name == 'user-posts'
        assert resolve(path).func.view_class == UserPostListView


    def test_blog_home_url(self):
        path = reverse('blog-home')
        assert resolve(path).view_name == 'blog-home'
        assert resolve(path).func.view_class == PostListView

