from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Post, Group
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm


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
    context = {
        "page_obj": page_obj,
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

def feedback_success(request):
    return render(request, "post_maker/feedback_success.html")

