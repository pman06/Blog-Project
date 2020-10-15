from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm, PostDeleteForm


# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'section':'home','posts':posts})

def detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/detail.html', {'section':'blog_detail','post':post})

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:details', slug= post.slug)

    else:
        form = PostForm()

    return render(request, 'blog/create.html',{'section': 'blog_create','form':form})

def edit(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:details', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit.html', {'section':'blog_edit','form':form, 'post':post})


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
