from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
import uuid

from apps.category.models import Category
from django.conf import settings

User = settings.AUTH_USER_MODEL


def blog_thumbnail_directory(instance, filename):
    return "blog/{0}/{1}".format(instance.title, filename)


# Create your models here.
class Post(models.Model):
    class Meta:
        ordering = ("-published",)

    class PostObjects(models.Manager):
        def get_queryset(self) -> QuerySet:
            return super().get_queryset().filter(status="published")

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255, default="New Post")
    slug = models.SlugField(max_length=255, unique=True, default=uuid.uuid4)
    thumbnail = models.ImageField(
        upload_to=blog_thumbnail_directory, max_length=500, blank=True, null=True
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    description = models.TextField(
        max_length=255, default="Enter a brief description here..."
    )
    content = RichTextField(default="Start writing your content here...")

    time_read = models.IntegerField(blank=True, null=True)

    published = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)

    status = models.CharField(max_length=10, choices=options, default="draft")

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, null=True
    )

    objects = models.Manager()  # default manager
    post_objects = PostObjects()  # custom manager

    def __str__(self) -> str:
        return self.title

    def get_view_count(self):
        views = ViewCount.objects.filter(post=self).count()
        return views


class ViewCount(models.Model):
    post = models.ForeignKey(
        Post, related_name="post_view_count", on_delete=models.CASCADE
    )
    ip_address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.ip_address}"
