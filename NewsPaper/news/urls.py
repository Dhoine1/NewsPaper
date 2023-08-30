from django.urls import path
from .views import PostList, PostDetail, index, PostSearch

urlpatterns = [
    path('', PostList.as_view(), name="Articles"),
    path('search/', PostSearch.as_view()),
    path('<int:pk>', PostDetail.as_view(), name="Post"),
    path('index/', index),
    ]