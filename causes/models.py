from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver


def upload_location(instance, filename):
    file_path = 'causes/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str (instance.title), filename=filename)
    return file_path


class BlogPost(models.Model):
    ENVIRONMENTAL = 'environmental'
    POLITICAL = 'political'
    EDUCATIONAL = 'educational'
    SPIRITUAL = 'spiritual'
    PHILOSOPHICAL = 'philosophical'
    OCCULT = 'occult'
    RECREATIONAL = 'recreational'
    CATEGORIES = [
        ('ENVIRONMENTAL',  ('Environmental')),
        ('POLITICAL',  ('Political')),
        ('EDUCATIONAL',  ('Educational')),
        ('SPIRITUAL',  ('Spiritual')),
        ('PHILOSOPHICAL',  ('Philosophical')),
        ('OCCULT',  ('Occult')),
        ('RECREATIONAL',  ('Recreational')),
        ]
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="cause_likes")
    category = models.CharField(max_length=32,choices=CATEGORIES,default='ENVIRONMENTAL', blank=False)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("causes:detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("causes:like-toggle", kwargs={"slug": self.slug})


@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs) :
    instance.image.delete (False)


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name="replies", on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))


pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)



# Create your models here.

