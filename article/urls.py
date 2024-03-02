from django.urls import path
from .views import Home, Post, About, ContactUsView, Posts, CategoryDetail, Search


app_name = 'article'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('post/<slug:slug>', Post.as_view(), name='post'),
    path('about', About.as_view(), name='about'),
    path('contact', ContactUsView.as_view(), name='contact'),
    path('posts', Posts.as_view(), name="posts"),
    path('catrgory/<slug:slug>', CategoryDetail.as_view(), name='category_detail'),
    path('search', Search.as_view(), name='search'),
]
