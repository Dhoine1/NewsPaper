from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment
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


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'NW'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'NW'
        return super().form_valid(form)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('Articles')


class ArticlesCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'AR'
        return super().form_valid(form)

class ArticlesUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.news_type = 'AR'
        return super().form_valid(form)


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('Articles')