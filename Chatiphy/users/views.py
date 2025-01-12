from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FormCreation, ProfileForm
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, get_object_or_404, redirect
from post_maker.models import Post
from post_maker.views import paginator, Subscription
from taggit.models import Tag


class SignUp(CreateView):
    # Define form class
    form_class = FormCreation
    # Redirecting to main page after successful register
    success_url = reverse_lazy("users:login")
    template_name = "users/signup.html"

    def form_valid(self, form):
        return super().form_valid(form)

class PasswordReset(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        error_message = False
        if not User.objects.filter(email=email).exists():
            error_message = True
            return render(self.request, self.template_name, {"form":form, "error_message":error_message})
        return super().form_valid(form)
    
def logout_view(request):
    logout(request)
    context = {}
    return render(request, "users/logged_out.html", context)


@login_required
def profile(request, username, tag_slug=None):
    template = "users/profile.html"
    user = get_object_or_404(User, username=username)
    profile = user.profile
    tag = None
    posts = Post.objects.filter(author=user).order_by("-pub_date")
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tag__in=[tag])
    latest = posts.latest("pub_date")
    latest_text = latest.text
    count = posts.count()
    page_obj = paginator(request, posts, 5)
    subscriptions = Subscription.objects.filter(subscriber=request.user).values_list('sub_author', flat=True)
    is_owner = request.user == user

    context = {"profile":profile,
               "username":username,
               "count":count,
               "page_obj":page_obj,
               "latest":latest,
               "latest_text":latest_text,
               "user":user,
               "tag":tag,
               'is_subscribed': user.id in subscriptions,
               "is_owner": is_owner}
    return render(request, template, context)

@login_required
def edit_profile(request, username):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form, "username":username})