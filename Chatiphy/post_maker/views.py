from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F, Q
from .models import Post, Group, Subscription
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CreatePostForm, CreateCommentForm
from taggit.models import Tag
from django.db.models import Count


@login_required
def index(request, tag_slug=None):
    filter_option = request.GET.get("filter", "all")
    tag = None
    if filter_option == "followed":
        followed_authors = Subscription.objects.filter(subscriber=request.user).values_list("sub_author", flat=True)
        posts = Post.objects.filter(author__in=followed_authors)
        show_followed = True
    elif filter_option == "all":
        posts = Post.objects.all().order_by("-pub_date")
        show_followed = False
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tag__in=[tag])
    template = "post_maker/index.html"
    page_obj = paginator(request, posts, 5)
    context = {
        "page_obj": page_obj,
        "show_followed":show_followed,
        "tag":tag
    }
    return render(request, template, context)

def search_field(request, tag_slug=None):
    query = request.GET.get('q', '').strip()
    tag = None
    results = Post.objects.all()
    if query:
        results = Post.objects.annotate(
            title_similarity=TrigramSimilarity('title', query),
            text_similarity=TrigramSimilarity('text', query),
            author_similarity=TrigramSimilarity('author__username', query),
            combined_similarity=F('title_similarity')+F('text_similarity')+F('author_similarity')
        ).filter(Q(title_similarity__gt=0.1)|Q(text_similarity__gt=0.1)|Q(author_similarity__gt=0.1)).order_by('-combined_similarity')
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        results = results.filter(tag__in=[tag])
    count = results.count()
    page_obj = paginator(request, results, 5)
    return render(request,
                  'post_maker/search.html',
                  {
                      'query': query,
                      'page_obj': page_obj,
                      'tag': tag,
                      'count': count
                  })
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
def group_posts_page(request, page, tag_slug=None):
    template = "post_maker/group_posts_page.html"
    group = get_object_or_404(Group, slug=page)
    tag = None
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tag__in=[tag])
    page_obj = paginator(request, posts, 5)
    context = {
        "group": group,
        "page_obj":page_obj,
        "tag":tag
    }
    return render(request, template, context)





@login_required
def post_detail(request, post_id, slug):
    template = "post_maker/post_detail.html"
    post = get_object_or_404(Post, pk=post_id, slug=slug)
    comments = post.comments.filter(active=True)
    form = CreateCommentForm()
    post_tags_ids = post.tag.values_list("id", flat=True)
    similar_posts = Post.objects.filter(tag__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags', '-pub_date')[:4]
    context = {"post":post,
               "comments":comments,
               "form":form,
               "similar_posts":similar_posts}
    return render(request, template, context)
    
@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
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
    return redirect("users:profile", username)

@login_required
def unsubscribe(request, username):
    sub_author = get_object_or_404(User, username=username)
    if request.user != sub_author:
        Subscription.objects.filter(subscriber=request.user, sub_author=sub_author).delete()
        request.user.follow = False
    return redirect("users:profile", username)
@login_required
def paginator(request, posts, pages):
    paginator_obj = Paginator(posts, pages)
    page_number = request.GET.get('page')
    return paginator_obj.get_page(page_number)