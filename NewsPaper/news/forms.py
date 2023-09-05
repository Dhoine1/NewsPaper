from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class NewsForm(forms.ModelForm):

    class Meta:
       model = Post
       fields = [
           'author',
           'cat_subject',
           'article_header',
           'article_text',
       ]

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name='authors')
        user.groups.add(authors)
        return user
