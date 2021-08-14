import datetime
import os.path

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django_comments_xtd.models import XtdComment
from taggit.managers import TaggableManager

from Users.models import User
from Yummy_site.settings import EMAIL_HOST_USER
from utility.Compress import compress_image


def Upload_path_for_blog(instance, filename):
    return os.path.join('Blog', instance.title, filename)


def custom_image_validator(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path filename
    valid = ['.jpg', '.png']
    if ext not in valid:
        raise ValidationError("Unsupported file extension.")


class Blog(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=16, help_text="Maximum length is 16")
    tags = TaggableManager()
    picture = models.ImageField(upload_to=Upload_path_for_blog,
                                validators=[custom_image_validator],
                                help_text="Valid extension's are JPG,PNG")
    blog_text = models.TextField(max_length=1024, blank=False, null=False,
                                 help_text='Maximum length is 1024', )
    is_approved = models.BooleanField(default=False, verbose_name='Approved',
                                      help_text="Only approved blogs show on the 'blogs' page")
    is_primary = models.BooleanField(default=False, verbose_name='Primary',
                                     help_text='If checked: the blog is shown on the main page')
    created_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.picture = compress_image(self.picture)
        self.created_date = datetime.datetime.now()
        if self.is_approved and self.pk:
            subscribed_email = Subscriber.objects.all().values_list('email',
                                                                    flat=True)
            send_mail(subject="New blog",
                      message=f"New blog is posted in {self.created_date}\n\n"
                              f"{self.blog_text[:20]}...",
                      from_email=EMAIL_HOST_USER,
                      recipient_list=subscribed_email,
                      )
        super(Blog, self).save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_blog', args=[str(self.id)])


class CustomComment(XtdComment):
    page = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.page = Blog.objects.get(pk=self.object_pk)
        super(CustomComment, self).save()


class Subscriber(models.Model):
    email = models.EmailField()
