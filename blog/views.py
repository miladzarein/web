from django.shortcuts import render, get_object_or_404
from blog.models import Comment, Post
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from taggit.models import Tag
from blog.forms import CommentForm
# Create your views here.

def blog_view(request,author_username=None):
    posts = Post.objects.filter(status=1)
    if author_username:
        posts = posts.filter(author__username = author_username)


    posts = Paginator(posts,3)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(posts.num_pages)

    context = {'posts':posts}
    return render(request, 'blog/blog-home.html',context)





def blog_single(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    comments = Comment.objects.filter(post=post, approved=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            
            form = CommentForm()  # فرم خالی برای ارسال جدید
    else:
        form = CommentForm()
    
    return render(request, 'blog/blog-single.html', {
        'post': post, 
        'comments': comments, 
        'form': form
    })

def blog_tag(request, tag_name):
    # پیدا کردن تگ بر اساس نام (با پشتیبانی از فارسی)
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(status=1, tags=tag)
    
    posts = Paginator(posts, 3)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(posts.num_pages)
    
    context = {'posts': posts, 'tag_name': tag_name}
    return render(request, 'blog/blog-home.html', context)


def blog_category(request,cat_name):
    posts = Post.objects.filter(status=1)
    posts = Post.objects.filter(category__name=cat_name)
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html',context)




def blog_search(request):
    posts = Post.objects.filter(status=1)

    if request.method == "GET":
        if s := request.GET.get('s'):
            posts = posts.filter(content__contains=s)
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html',context)
