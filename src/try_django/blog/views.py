from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404


# Create your views here.
from .models import BlogPost, Post, Comment
from .forms import BlogPostModelForm
from .forms import *

def blog_post_detail_page(request, slug):
    # obj =BlogPost.objects.get(id=post_idv)
    #queryset = BlogPost.objects.filter(slug=slug)
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name='blog_post_detail_page.html'
    context = {'object':obj}
    return render(request, template_name, context)

def blog_post_list_view(request):
    qs = BlogPost.objects.all().published()
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        user = (qs|my_qs).distinct()
    template_name='blog/list.html'
    context = {'object_list':qs}
    return render(request, template_name, context)

# @login_required()
@staff_member_required
def blog_post_create_view(request):
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()
    template_name='form.html'
    context = {'form':form}
    return render(request, template_name, context)

# @staff_member_required
def blog_post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    obj = get_object_or_404(BlogPost,slug=slug)
    comments = Comment.objects.filter(post=post)
    template_name='blog/detail.html'
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'object':obj,
        'post':post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments':comments,
    }
    return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    template_name='form.html'
    context = {"title": f"Update{obj.title}", 'form':form}
    return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name='blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {'object':obj}
    return render(request, template_name, context)
