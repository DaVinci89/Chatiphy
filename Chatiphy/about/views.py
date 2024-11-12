from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm

class AboutAuthorView(TemplateView):
    template_name = "about/author.html"
    
class AboutTechView(TemplateView):
    template_name = "about/tech.html"

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
            return redirect("about:feedback_success")
        return render(request, "about/feedback.html", {"form":form})
    form = FeedbackForm()
    return render(request, "about/feedback.html", {"form":form})

@login_required
def feedback_success(request):
    return render(request, "post_maker/feedback_success.html")
