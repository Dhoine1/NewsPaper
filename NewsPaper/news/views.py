from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from .models import Post, Comment, Subscription, Category
from django.shortcuts import render
from .filters import PostFilter
from .forms import NewsForm


class PostList(ListView):
    model = Post
    ordering = 'create_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


def index(request):
    com = Comment.objects.all()
    return render(request, 'index.html', context={'com': com})


class PostSearch(ListView):
    model = Post
    ordering = 'create_date'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.GET:
            queryset = super().get_queryset()
            self.filterset = PostFilter(self.request.GET, queryset)
            return self.filterset.qs
        else:
            queryset = Post.objects.none()
            self.filterset = PostFilter(self.request.GET, queryset)
            return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'NW'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    raise_exception = True
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'NW'
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('Articles')
    permission_required = ('news.delete_post',)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'AR'
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'AR'
        return super().form_valid(form)


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('Articles')
    permission_required = ('news.delete_post',)

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        user = request.user

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('subject')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )