from django import template
from django.utils import timezone
from django.db.models import Count

from ..models import Post



register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.filter(published_date__lte=timezone.now()).count()

@register.inclusion_tag('blog/_post_list.html')
def post_include(count):
    latest = Post.objects.filter(published_date__lte=timezone.now())[:count]
    return {'latest_posts':latest}

@register.simple_tag
def get_most_commentted_posts(count=5):
    total_comment = Post.objects.filter(published_date__lte=timezone.now()).annotate(total_comment= Count('comments')).order_by('-total_comment')[:count]
    return total_comment
