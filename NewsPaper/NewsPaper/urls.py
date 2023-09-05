from django.contrib import admin
from django.urls import path, include
from news.views import  NewsCreate, NewsUpdate, NewsDelete, ArticlesCreate, ArticlesUpdate, ArticlesDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path("accounts/", include("allauth.urls")),

    path('news/create/', NewsCreate.as_view(), name='News_Create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='News_Update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='News_Delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='News_Create'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='News_Update'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='News_Delete'),
]
