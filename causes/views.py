from django.shortcuts import render, redirect, get_object_or_404

from causes.models import BlogPost, Comment
from causes.forms import CreateCausePostForm, UpdateCausePostForm, CommentForm
from account.models import Account
from django.views.generic import RedirectView
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def create_causes_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateCausePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateCausePostForm()

    context['form'] = form

    return render(request, "causes/create_cause.html", context)


def detail_causes_view(request, slug):
    causes_post = get_object_or_404(BlogPost, slug=slug)
    comments = Comment.objects.filter(post=causes_post, reply=None).order_by()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=causes_post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            return HttpResponseRedirect(causes_post.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'causes_post': causes_post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'causes/detail_causes.html', context)


class CauseLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        obj = get_object_or_404 (BlogPost, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


def edit_causes_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    causes_post = get_object_or_404(BlogPost, slug=slug)
    if request.POST:
        form = UpdateCausePostForm(request.POST or None, request.FILES or None, instance=causes_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            causes_post = obj
    form = UpdateCausePostForm(
        initial = {
            "title": causes_post.title,
            "body": causes_post.body,
            "image": causes_post.image,
        }
    )

    context['form'] = form
    return render(request, 'causes/edit_cause.html', context)


def delete_causes_view(request, slug):

    cause = get_object_or_404(BlogPost, slug=slug)
    if request.user == cause.author:
        cause.delete()
        return redirect('home')
