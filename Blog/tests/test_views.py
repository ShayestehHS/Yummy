import io
import json

from PIL import Image
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from Blog.models import Blog, Subscriber


def generate_photo_file(pic_format='.png'):
    file = io.BytesIO()
    image = Image.new('RGBA', (800, 1200), (255, 255, 255))
    image.save(file, 'png')
    file.name = 'test' + pic_format
    file.seek(0)
    return file


class PublicBlogViewsTest(TestCase):
    def setUp(self):
        user_data = {
            'username': 'BlogViewUsername',
            'email': 'public@email.com',
            'first_name': 'test',
            'last_name': 'testian',
            'password': 'Password123',
        }
        blog_data = {
            'title': 'blog test',
            'blog_text': 'SetUp test blog text',
            'is_approved': True, 'is_primary': True,
        }

        self.client = Client()
        self.picture = generate_photo_file()
        self.user = get_user_model().objects.create_user(**user_data)
        self.blog = Blog.objects.create(author=self.user, picture=self.picture, **blog_data)

        super(PublicBlogViewsTest, self).setUp()

    def tearDown(self):
        super(PublicBlogViewsTest, self).tearDown()

    def test_all_primary_blogs_listing(self):
        """ Test all exists primary blogs are listing in blog_page """
        blog = Blog.objects.create(author=self.user, title='primary',
                                   blog_text='This is a long text', picture=self.picture,
                                   is_primary=True, is_approved=True, )

        res = self.client.get(reverse('list_blog', kwargs={'page': 1}))
        blogs_titles = [blog.title for blog in res.context['blogs']]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'blog/blogs.html')
        self.assertEqual(len(blogs_titles), 2)
        self.assertEqual(blogs_titles, [self.blog.title, blog.title])

    def test_blog_detail_page_is_working(self):
        """ Test showing detail of blog in blog_detail_page is working correctly """
        res = self.client.get(reverse('detail_blog',
                                      kwargs={'blog_id': self.blog.id, }))
        detail_blog = res.context['blog']

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'blog/post_detail.html')
        self.assertEqual(detail_blog, self.blog)
        self.assertIsNotNone(res.context['recent'])

    def test_blog_tag_search_is_working(self):
        """ Test filtering blogs by their tags in blog_tag_search working correctly """
        blog_data = {
            'author': self.user,
            'title': 'blog tag search',
            'picture': self.picture,
            'blog_text': 'This is a long text',
            'is_approved': True,
        }

        self.blog.tags.add('test_tag')
        blog = Blog.objects.create(**blog_data)
        blog.tags.add('testing_tag')

        res = self.client.get(reverse('blog_tagSearch', kwargs={'tag_slug': 'test_tag',
                                                                'page': 1, }))
        res_blogs = res.context['blogs']

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'blog/blogs.html')
        self.assertEqual(len(res_blogs), 1)
        self.assertEqual(res_blogs[0].title, self.blog.title)

    def test_blog_search_is_working(self):
        """ Test search functionality of blog_search is working correctly """
        res = self.client.post(reverse('blog_search'), data={
            'searched_key': self.blog.title, })

        founded_blogs = res.context['blogs']

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(res, 'blog/blogs.html')
        self.assertGreaterEqual(len(founded_blogs), 1)
        self.assertIn(self.blog, list(founded_blogs))

    def test_blog_search_with_None_data_is_fail(self):
        """ Test to not sending any data to blog_search and redirect to list_blog page """
        res = self.client.post(reverse('blog_search'))

        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res['location'], reverse('list_blog', kwargs={'page': 1}))

    def test_subscribe_AJAX_with_non_exists_email(self):
        """ Test subscription with valid email is working fine """
        res = self.client.post(reverse('subscribe'), data={'email': "AJAX@test.com"},
                               content_type='application/json',
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest', )
        AJAX_res = str(res.content, encoding='utf8')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(json.dumps({'success': "Subscription was successfully"}),
                             AJAX_res)

    def test_subscribe_AJAX_with_exists_email(self):
        """ Test subscription with exist email is fail """
        test_mail = 'first@email.com'
        Subscriber.objects.create(email=test_mail)
        res = self.client.post(reverse('subscribe'), data={'email': test_mail},
                               content_type='application/json',
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest', )

        AJAX_res = str(res.content, encoding='utf8')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(json.dumps({'error': "you can't subscribe again"}), AJAX_res)
