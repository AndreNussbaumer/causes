from django import forms
from causes.models import BlogPost, Comment


class CreateCausePostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'category']


class UpdateCausePostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'category']

    def save(self, commit=True):
        causes_post = self.instance
        causes_post.title = self.cleaned_data['title']
        causes_post.body = self.cleaned_data['body']
        causes_post.category = self.cleaned_data['category']

        if self.cleaned_data['image']:
            causes_post.image = self.cleaned_data['image']

        if commit:
            causes_post.save()
        return causes_post


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = {'content',}