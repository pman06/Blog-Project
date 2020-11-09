from blog.models import Post
from django.utils import timezone

def latest_posts(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-created_date')[:10]
    return {'latest_posts':posts}
