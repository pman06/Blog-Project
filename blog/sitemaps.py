from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.objects.filter(published_date__lte=timezone.now())

    def lastmod(self, obj):
        return obj.updated_date
