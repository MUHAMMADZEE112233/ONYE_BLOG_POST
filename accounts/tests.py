from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from .forms import CommentForm, CustomUserChangeForm, PostForm
from .models import Post, Category, Comment

User = get_user_model()


class BlogPostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')
        self.category = Category.objects.create(name='Test Category')
        self.blog_post = Post.objects.create(
            title='Test Title', content='Test Content', author=self.user, category=self.category)

    def test_blog_post_creation(self):
        self.assertEqual(self.blog_post.title, 'Test Title')
        self.assertEqual(self.blog_post.content, 'Test Content')
        self.assertEqual(self.blog_post.author, self.user)
        self.assertEqual(self.blog_post.category, self.category)


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')
        self.category = Category.objects.create(name='Test Category')
        self.blog_post = Post.objects.create(
            title='Test Title', content='Test Content', author=self.user, category=self.category)
        self.comment = Comment.objects.create(
            post=self.blog_post, name='Commenter', email='commenter@example.com', body='Test Comment')

    def test_comment_creation(self):
        self.assertEqual(self.comment.post, self.blog_post)
        self.assertEqual(self.comment.name, 'Commenter')
        self.assertEqual(self.comment.email, 'commenter@example.com')
        self.assertEqual(self.comment.body, 'Test Comment')


class CustomUserChangeFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '1990-01-01',
        }
        form = CustomUserChangeForm(data=form_data)
        self.assertTrue(form.is_valid())




class BlogPostFormTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_valid_form(self):
        form_data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'category': self.category.id,
        }
        form = PostForm(data=form_data)

        self.assertTrue(form.is_valid())


class CommentFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'name': 'Commenter',
            'email': 'commenter@example.com',
            'body': 'Test Comment',
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())


class ProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('profile')

    def test_profile_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')


class EditProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')
        self.client.login(email='testuser@example.com', password='password123')
        self.url = reverse('edit_profile')

    def test_edit_profile_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

    def test_edit_profile_post(self):
        form_data = {
            'email': 'newemail@example.com',
            'first_name': 'New',
            'last_name': 'Name',
            'date_of_birth': '1990-01-01',
        }
        response = self.client.post(self.url, data=form_data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.first_name, 'New')
        self.assertEqual(self.user.last_name, 'Name')


class BlogPostViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')
        self.category = Category.objects.create(name='Test Category')
        self.blog_post = Post.objects.create(
            title='Test Title', content='Test Content', author=self.user, category=self.category)

    def test_latest_blog_posts_view(self):
        url = reverse('latest_blog_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/latest_blog_posts.html')
        self.assertContains(response, 'Test Title')

    def test_post_detail_view(self):
        url = reverse('post_detail', args=[self.blog_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/post_detail.html')
        self.assertContains(response, 'Test Title')


class CommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com', password='password123')
        self.category = Category.objects.create(name='Test Category')
        self.blog_post = Post.objects.create(
            title='Test Title', content='Test Content', author=self.user, category=self.category)

    def test_add_comment(self):
        url = reverse('post_detail', args=[self.blog_post.id])
        form_data = {
            'name': 'Commenter',
            'email': 'commenter@example.com',
            'body': 'Test Comment',
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your comment has been added!')
