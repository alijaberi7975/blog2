from builtins import filter

from django.contrib import admin
from .models import Category, Article, AboutMe, ContactUs, Comment, Like, FavoriteArticle


class CommentAdmin(admin.TabularInline):
    model = Comment


@admin.register(Category)
class CategoryAmin(admin.ModelAdmin):
    list_display = ('title', 'slug')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status')
    list_filter = ('status',)
    inlines = (CommentAdmin,)


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    filter = ('status', 'author')


admin.site.register(ContactUs)
admin.site.register(Like)
admin.site.register(FavoriteArticle)