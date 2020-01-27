from django.shortcuts import render
from operator import attrgetter
from causes.models import BlogPost
# Create your views here. View - Template - Url


def home_screen_view(request, *args, **kwargs):

    context = {}

    causes_post = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'))
    context['causes_post'] = causes_post

    return render(request, "personal/home.html", context)