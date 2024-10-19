from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf import settings
from .models import Post, Group, Comment
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm, CreatePostForm, CreateCommentForm


def index(request):
    keyword = request.GET.get("q", None)
    if keyword:
        posts = Post.objects.filter(text__contains=keyword).select_related("author").order_by("-pub_date")
    else:
        posts = Post.objects.order_by("-pub_date")
    template = "post_maker/index.html"
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    show_toast = request.session.pop('show_toast', False)
    context = {
        "page_obj": page_obj,
        "show_toast":show_toast,
    }
    return render(request, template, context)


def group_posts(request):
    template = "post_maker/group_posts.html"
    text = "<h2><b>Groups</b><h2>"
    groups = Group.objects.all()
    groups_count = Group.objects.count()
    paginator = Paginator(groups, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "header": text,
        "page_obj":page_obj,
        "groups_count":groups_count
    }
    return render(request, template, context)

@login_required
def group_posts_page(request, page):
    template = "post_maker/group_posts_page.html"
    group = get_object_or_404(Group, slug=page)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "page_obj":page_obj,
    }
    return render(request, template, context)

@login_required
def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["body"]
            send_mail( f'New Feedback Form {subject} from {name}',
                f'Message: {message}\n\nFrom: {name} ({email})',
                settings.DEFAULT_FROM_EMAIL,
                ['workdavinci39@gmail.com'],
                fail_silently=False)
            return redirect("post_maker:feedback_success")
        return render(request, "post_maker/feedback.html", {"form":form})
    form = FeedbackForm()
    return render(request, "post_maker/feedback.html", {"form":form})

@login_required
def feedback_success(request):
    return render(request, "post_maker/feedback_success.html")

@login_required
def profile(request, username):
    template = "post_maker/profile.html"
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by("-pub_date")
    latest = posts.latest("pub_date")
    latest_text = latest.text
    count = posts.count()
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"username":username,
               "count":count,
               "page_obj":page_obj,
               "latest":latest,
               "latest_text":latest_text}
    return render(request, template, context)

@login_required
def post_detail(request, post_id):
    template = "post_maker/post_detail.html"
    post = get_object_or_404(Post, pk=post_id)
    context = {"post":post,}
    return render(request, template, context)
    
@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_maker:profile", username = request.user.username)
    else:
        form = CreatePostForm()
    return render(request, "post_maker/create_post.html", {"form":form})
    
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("post_maker:post_detail", post_id=post.pk)
    if request.method == "POST":
        form = CreatePostForm(request.POST, files=request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_maker:post_detail", post_id=post.pk)
    else:
        form = CreatePostForm(instance=post)
    context = {"form":form, "is_edit":True, "post":post}
    return render(request, "post_maker/create_post.html", context)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment = None
    form = CreateCommentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = request.post
        comments = Comment.objects.filter(post=comment.post)
        comment.save()
    context = {
        "post":post,
        "form":form,
        "comment":comment,
        "comments": comments,
    }
    return render(request,"post_maker/comment.html", context)
            

