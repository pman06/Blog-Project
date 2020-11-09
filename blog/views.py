from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, TemplateView, DetailView,
                                CreateView, UpdateView, DeleteView)
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import PostForm, PostDeleteForm, CommentForm, EmailPostForm

from taggit.models import Tag



# Create your views here.

class Home(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'home.html'
    paginate_by = 3

    def get_queryset(self):
        if self.kwargs.get('tag'):
            tag = self.kwargs.get('tag')
            queryset = Post.objects.filter(tags__slug=tag, published_date__lte= timezone.now())
        else:
            queryset = Post.objects.filter(published_date__lte= timezone.now())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'home'
        if self.kwargs.get('tag'):
            context['tag'] = self.kwargs.get('tag')
        return context

'''
def home(request, tag=None):
    tag_obj = None

    if not tag:
        posts = Post.objects.all().order_by('-created_date')
    else:
        tag_obj =get_object_or_404(Tag, slug=tag)
        posts = Post.objects.filter(tags__in=[tag_obj]).order_by('-created_date')

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'home.html', {'section':'home','posts':posts, 'tag':tag_obj})
'''

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog_detail'
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        context['comments'] = post.approve_comments()

        #get all similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids, published_date__lte= timezone.now()).exclude(id=post.id)
        context['similar_posts'] = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-published_date')[:4]
        return context

'''
def detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/detail.html', {'section':'blog_detail','post':post})
'''

class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    #fields = ['title', 'body', 'image']
    template_name = 'blog/create.html'
    login_url = '/login/'
    redirect_field_name = '/'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog_create'
        return context

'''
@permission_required('blog.add_post', raise_exception= True)
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:details', slug= post.slug)

    else:
        form = PostForm()

    return render(request, 'blog/create.html',{'section': 'blog_create','form':form})
'''


class PostEditView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'blog/edit.html'
    #fields = ['title', 'body', 'image']
    login_url = '/login/'
    redirect_field_name = '/'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'blog_create'
        return context


'''
@permission_required('blog.change_post', raise_exception=True)
def edit(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:details', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit.html', {'section':'blog_edit','form':form, 'post':post})
'''

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'blog/delete.html'

'''
@permission_required('blog.delete_post', raise_exception=True)
def delete(request, pk=None):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post)
        if form.is_valid():
            post.delete()
            return redirect('home')

    else:
        form = PostDeleteForm(instance = post)

    return render(request,'blog/delete.html' ,{'section':'blog_delete','form':form, 'post':post})
'''

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'next'
    model = Post
    template_name= 'blog/post_draft_list.html'
    context_object_name = 'draft_posts'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'about'
        return context

class About(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'about'
        return context



#####################################################
#####################################################
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published()
    return redirect('blog:details', slug=post.slug )


def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            if comment:
                print("Comment added successfully: ", comment)
            return redirect('blog:details', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect(comment.post.get_absolute_url())

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    comment.delete()
    return redirect(post.get_absolute_url())


def post_share(request, id):
    post = get_object_or_404(Post, id=id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n \n {cd['name']}\'s comments:{cd['comments']}"
            send = send_mail(subject, message, 'admin@myblog.com', [cd['to_email']])
            print('Sent:  ',send)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'form':form, 'post':post, 'sent':sent})
