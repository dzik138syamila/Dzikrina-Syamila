# blog/models.py

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100)
 
    def __str__(self):
        return self.category

class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='page_images/')
    slug = models.SlugField(unique=True, max_length=255)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField(choices=[
        (0, 'Draft'),
        (1, 'Published'),
    ], default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
