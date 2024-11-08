from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf import settings
from .models import Post, Group, Subscription
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import FeedbackForm, CreatePostForm, CreateCommentForm


@login_required
def index(request):
    filter_option = request.GET.get("filter", "all")
    keyword = request.GET.get("q", None)
    if filter_option == "followed":
        followed_authors = Subscription.objects.filter(subscriber=request.user).values_list("sub_author", flat=True)
        posts = Post.objects.filter(author__in=followed_authors)
        show_followed = True
    elif filter_option == "all":
        posts = Post.objects.all().order_by("-pub_date")
        show_followed = False
    if keyword:
        posts = Post.objects.filter(text__contains=keyword).select_related("author").order_by("-pub_date")
    template = "post_maker/index.html"
    page_obj = paginator(request, posts, 5)
    context = {
        "page_obj": page_obj,
        "show_followed":show_followed
    }
    return render(request, template, context)


def group_posts(request):
    template = "post_maker/group_posts.html"
    text = "<h2><b>Groups</b><h2>"
    groups = Group.objects.all()
    groups_count = Group.objects.count()
    page_obj = paginator(request, groups, 5)
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
    page_obj = paginator(request, posts, 5)
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
    page_obj = paginator(request, posts, 5)
    subscriptions = Subscription.objects.filter(subscriber=request.user).values_list('sub_author', flat=True)

    context = {"username":username,
               "count":count,
               "page_obj":page_obj,
               "latest":latest,
               "latest_text":latest_text,
               "user":user,
               'is_subscribed': user.id in subscriptions,}
    return render(request, template, context)

@login_required
def post_detail(request, post_id, slug):
    template = "post_maker/post_detail.html"
    post = get_object_or_404(Post, pk=post_id, slug=slug)
    comments = post.comments.filter(active=True)
    form = CreateCommentForm()
    context = {"post":post,
               "comments":comments,
               "form":form}
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
def edit_post(request, post_id, slug):
    post = get_object_or_404(Post, pk=post_id, slug=slug)
    if request.user != post.author:
        return redirect("post_maker:post_detail", post_id=post.id, slug=post.slug)
    if request.method == "POST":
        form = CreatePostForm(request.POST, files=request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_maker:post_detail", post_id=post.id, slug=post.slug)
    else:
        form = CreatePostForm(instance=post)
    context = {"form":form, "is_edit":True, "post":post}
    return render(request, "post_maker/create_post.html", context)

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CreateCommentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("post_maker:post_detail", post_id=post_id, slug=post.slug)

@login_required
def subscribe(request, username):
    sub_author = get_object_or_404(User, username=username)
    if request.user != sub_author:
        Subscription.objects.get_or_create(subscriber=request.user, sub_author=sub_author)
        request.user.follow = True
    return redirect("post_maker:profile", username)

@login_required
def unsubscribe(request, username):
    sub_author = get_object_or_404(User, username=username)
    if request.user != sub_author:
        Subscription.objects.filter(subscriber=request.user, sub_author=sub_author).delete()
        request.user.follow = False
    return redirect("post_maker:profile", username)
@login_required
def paginator(request, posts, pages):
    paginator_obj = Paginator(posts, pages)
    page_number = request.GET.get('page')
    return paginator_obj.get_page(page_number)