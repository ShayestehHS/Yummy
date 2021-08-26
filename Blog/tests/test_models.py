import io

from django.core.exceptions import ValidationError
from django.test import TestCase
from Blog.models import Blog
from django.contrib.auth import get_user_model
from PIL import Image
from taggit.models import Tag


def generate_photo_file(pic_format='.png'):
    file = io.BytesIO()
    image = Image.new('RGBA', (800, 1200), (255, 255, 255))
    image.save(file, 'png')
    file.name = 'test' + pic_format
    file.seek(0)
    return file


class PrivateModelTest(TestCase):
    def setUp(self):
        user_data = {
            'email': 'private@test.com',
            'username': 'modelUsername',
            'first_name': 'test',
            'last_name': 'testian',
            'password': 'Password123',
        }
        self.user = get_user_model().objects.create_user(**user_data)
        self.image = generate_photo_file()

        super(PrivateModelTest, self).setUp()

    def tearDown(self):
        super(PrivateModelTest, self).tearDown()

    def test_create_blog_is_successfully(self):
        """ Test creation blog with valid user is successfully """
        blog_data = {
            'author': self.user,
            'title': 'test title',
            'blog_text': 'This is a long text',
            'is_primary': True,
            'is_approved': True,
            'picture': self.image,
        }
        blog = Blog.objects.create(**blog_data)
        blog.tags.add('test')
        blog.tags.add('testing')

        filtered_blog = Blog.objects.get(title__iexact='test title')
        test_tag = Tag.objects.filter(name__in=['test', 'testing'])

        self.assertEqual(filtered_blog.author, self.user)
        self.assertIsNotNone(filtered_blog.picture)
        self.assertEqual(list(test_tag), list(filtered_blog.tags.all()))

    def test_create_blog_with_exists_title(self):
        """ Test creation new blog with exists title is fail """
        blog_title = 'test title'
        blog1_data = {
            'author': self.user,
            'title': blog_title,
            'blog_text': 'This is a long text',
            'picture': self.image,
        }
        Blog.objects.create(**blog1_data)

        with self.assertRaisesRegex(ValidationError, 'Blog with this Title already exists.'):
            blog2_data = {
                'author': self.user,
                'title': blog_title,
                'blog_text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                'picture': self.image,
            }
            Blog.objects.create(**blog2_data)

        self.assertEqual(Blog.objects.filter(title=blog_title).count(), 1)

    def test_create_blog_with_invalid_picture(self):
        """ Test creation Blog with invalid picture type fails """
        with self.assertRaisesRegex(ValidationError, "Unsupported file extension."):
            Blog.objects.create(
                author=self.user,
                title='invalid picture',
                blog_text='This is a long text',
                picture=generate_photo_file('.rgb')
            )

        self.assertEqual(Blog.objects.filter(title='invalid picture format').count(), 0)

    def test_create_blog_with_long_title(self):
        """ Test creation Blog with title length more than 16 is failing. """
        blog_title = 'This is long title(more than 16 character)'
        with self.assertRaisesRegex(ValidationError, f"Ensure this value has at most 16 characters "
                                                     f"\(it has {len(blog_title)}\)."):
            Blog.objects.create(
                author=self.user,
                title=blog_title,
                blog_text='This is a long text',
                picture=generate_photo_file())

        self.assertEqual(Blog.objects.filter(title='invalid picture format').count(), 0)
