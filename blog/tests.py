from django.urls import reverse
from django.test import TestCase
from blog.models import Category, Blog
from users.models import User


class CategoryTests(TestCase):
    """Тесты для модели Category."""

    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_create(self):
        """Тест на создание категории"""
        self.assertEqual(self.category.name, 'Test Category')

    def test_category_str(self):
        """Тест на строковое представление категории"""
        self.assertEqual(str(self.category), 'Test Category')


class BlogModelTests(TestCase):
    """Тесты для модели Blog."""

    def setUp(self):
        self.user = User.objects.create(phone='+71234567890', name='Test User')
        self.category = Category.objects.create(name='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='Test Content',
            author=self.user,
            category=self.category,
            is_published=True,
            is_subscribed=False,
        )

    def test_blog_create(self):
        """Тест на создание записи блога."""
        blog = Blog.objects.create(
            title='New Blog',
            content='New Content',
            author=self.user,
            category=self.category,
            is_published=True,
            is_subscribed=True,
        )
        self.assertEqual(blog.title, 'New Blog')
        self.assertEqual(blog.content, 'New Content')
        self.assertEqual(blog.author, self.user)
        self.assertEqual(blog.category, self.category)
        self.assertTrue(blog.is_published)
        self.assertTrue(blog.is_subscribed)

    def test_views_count_increments(self):
        """Тест на увеличение счетчика просмотров."""
        initial_views = self.blog.views_count
        self.blog.views_count += 1
        self.blog.save()
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.views_count, initial_views + 1)

    def test_is_published(self):
        """Тест на проверку статуса публикации блога."""
        self.assertTrue(self.blog.is_published)
        self.blog.is_published = False
        self.blog.save()
        self.blog.refresh_from_db()
        self.assertFalse(self.blog.is_published)

    def test_blog_created_at(self):
        """Тест на правильное сохранение времени создания блога."""
        self.assertIsNotNone(self.blog.created_at)
        self.assertLessEqual(self.blog.created_at, self.blog.updated_at)

    def test_blog_str(self):
        """Тест на строковое представление блога."""
        self.assertEqual(str(self.blog), 'Test Blog')


class BlogViewsTests(TestCase):
    """Тесты для представлений, связанных с блогами."""

    def setUp(self):
        self.user = User.objects.create(phone='+71234567890', name='Test User')
        self.category1 = Category.objects.create(name='Category')
        self.category2 = Category.objects.create(name='Category 1')

        self.blog1 = Blog.objects.create(
            title='Test Title 1',
            content='Test Content 1',
            author=self.user,
            category=self.category1,
            is_published=True,
            is_subscribed=False
        )
        self.blog2 = Blog.objects.create(
            title='Test Title 2',
            content='Test Content 2',
            author=self.user,
            category=self.category1,
            is_published=True,
            is_subscribed=False
        )
        self.blog3 = Blog.objects.create(
            title='Test Title 3',
            content='Test Content 3',
            author=self.user,
            category=self.category1,
            is_published=False,
            is_subscribed=False
        )
        self.client.force_login(self.user)

    def test_blog_list_view(self):
        """Тест на страницу списка блогов"""
        response = self.client.get(reverse('blog:blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')
        self.assertContains(response, 'Test Title 1')
        self.assertContains(response, 'Test Title 2')

        self.assertNotContains(response, 'Test Title 3')

    def test_blog_detail_view(self):
        """Тест на страницу детализации блога"""
        response = self.client.get(reverse('blog:detail', args=[self.blog1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title 1')
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.blog1.refresh_from_db()
        self.assertEqual(self.blog1.views_count, 1)

    def test_blog_create_view(self):
        """Тест на создание блога"""
        response = self.client.post(reverse('blog:create'), {
            'title': 'New Blog',
            'content': 'New Content',
            'category': self.category1.id,
            'is_published': True,
            'is_subscribed': False,
        })
        self.assertRedirects(response, reverse('blog:blog_list'))
        self.assertEqual(Blog.objects.count(), 4)

    def test_blog_update_view(self):
        """Тест на обновление блога"""
        response = self.client.post(reverse('blog:update', args=[self.blog1.id]), {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'is_published': True,
            'category': self.category1.id,
            'is_subscribed': False,
        })
        self.blog1.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.blog1.title, 'Updated Title')
        self.assertRedirects(response, reverse('blog:blog_list'))

    def test_blog_delete_view(self):
        """Тест на удаление блога"""
        response = self.client.post(reverse('blog:delete', args=[self.blog1.id]))
        self.assertRedirects(response, reverse('blog:blog_list'))
        self.assertFalse(Blog.objects.filter(id=self.blog1.id).exists())
        self.assertEqual(Blog.objects.count(), 2)

    def test_index_view_context(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('unique_authors', response.context)
        self.assertIn('total_posts', response.context)
        self.assertIn('unique_members', response.context)
        self.assertIn('random_posts', response.context)
        self.assertIn('is_subscribed', response.context)

    def test_contacts_view_get(self):
        response = self.client.get(reverse('blog:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/contacts.html')

    def test_contacts_view_post(self):
        response = self.client.post(reverse('blog:contacts'),
                                    {'name': 'Test', 'phone': '12345', 'message': 'Test message'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/contacts.html')

    def test_category_list_view(self):
        response = self.client.get(reverse('blog:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_list.html')
        self.assertContains(response, 'Category')
        self.assertContains(response, 'Category 1')

    def test_category_detail_view(self):
        response = self.client.get(reverse('blog:category_detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Title')
