from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
class Post(models.Model):

    title = models.CharField(default='', max_length= 255)
    body = models.TextField(default='',blank=True,)
    slug = models.SlugField(default='',blank=True, max_length= 255)
    date = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now = True, null=True)
    author = models.ForeignKey(User, null=True,blank=True,on_delete= models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:details', args=[str(self.slug)])
