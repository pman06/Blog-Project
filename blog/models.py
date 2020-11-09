from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name="blog_posts")
    title = models.CharField(default='', max_length= 255)
    body = models.TextField(default='',blank=True,)
    slug = models.SlugField(default='',blank=True, unique_for_date='published_date',max_length= 255)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    published_date =models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now = True, null=True)
    tags = TaggableManager()
    image = models.ImageField(default ='',blank =True, upload_to='images')
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(700,270)], format='JPEG', options={'quality':60})


    class Meta:
        ordering = ['-published_date']

    def published(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment = True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:details', args=[str(self.slug)])


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete= models.CASCADE, related_name = 'comments' )
    author = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now = True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('/')
