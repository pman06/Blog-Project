from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Post



class LatestPostsFeed(Feed):
    title ='My blog'
    link = reverse_lazy('home')
    description ='New posts of my blog.'

    def items(self):
        return Post.objects.filter(published_date__lte=timezone.now())

    def item_title(self, item):
        return item.title

    def item_description(self,item):
        return truncatewords(item.body, 30)
