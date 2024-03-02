from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, ListView, TemplateView
from .form import Contact, CommentForm
from .models import Article, AboutMe, ContactUs, Comment, Category, Like, FavoriteArticle
from django.contrib.auth.mixins import LoginRequiredMixin


# --------------------------------------------------------


class Home(View):
    def get(self, request):
        Articles = Article.objects.order_by('-created')[:6]
        return render(request, 'index.html', {'Articles': Articles})


# -------------------------------------------------------------------

class Post(View):
    comment_added = False

    def get(self, request, slug):
        if request.user.is_authenticated:
            article = Article.objects.filter(slug=slug).first()
            if article:
                comments = article.comments.filter(parent=None)
                form = CommentForm()
                liked = Like.objects.filter(user=request.user, article=article)
                is_saved = FavoriteArticle.objects.filter(user=request.user, article=article)
                return render(request, 'post.html', {'article': article, 'comments': comments, 'form': form,
                                                     'comment_added': self.comment_added, 'liked': liked,
                                                     'is_saved': is_saved})
            else:
                return redirect('article:home')
        else:
            return redirect('account:login')

    def post(self, request, slug):
        form = CommentForm(request.POST)
        article = Article.objects.get(slug=slug)
        comments = article.comments.filter(accept=True)
        id_parent = request.POST.get('parent_comment_id')
        comment = Comment.objects.get(id=id_parent) if id_parent else None

        # Handle like/unlike
        if 'action' in request.POST and request.POST['action'] == 'toggle_like':
            return self.toggle_like(request, article)

        # Handle favorite/unfavorite
        if 'action' in request.POST and request.POST['action'] == 'toggle_favorite':
            return self.toggle_favorite(request, article)

        if form.is_valid():
            if comment:
                Comment.objects.create(article=article, parent=comment, author=form.cleaned_data['author'],
                                       text=form.cleaned_data['text'], accept=False)
                self.comment_added = True
            else:
                Comment.objects.create(article=article, author=form.cleaned_data['author'],
                                       text=form.cleaned_data['text'])
                self.comment_added = True

            return render(request, 'post.html', {'article': article, 'form': form, 'comment_added': self.comment_added})
        else:
            return render(request, 'post.html', {'article': article, 'form': form})

    def toggle_like(self, request, article):
        like, created = Like.objects.get_or_create(user=request.user, article=article)
        if created:
            liked = True
        else:
            like.delete()
            liked = False

        response_data = {
            'like_count': Like.objects.filter(article=article).count(),
            'liked': liked,
        }
        return JsonResponse(response_data)

    def toggle_favorite(self, request, article):
        favorite, created = FavoriteArticle.objects.get_or_create(user=request.user, article=article)
        if created:
            is_favorite = True
        else:
            favorite.delete()
            is_favorite = False

        response_data = {
            'is_favorite': is_favorite,
        }
        return JsonResponse(response_data)


# ------------------------------------------------------------------------------


class About(View):
    def get(self, request):
        Me = AboutMe.objects.all().last()
        return render(request, 'about.html', {'me': Me})


# -------------------------------------------------------------------------------


class ContactUsView(FormView):
    def get(self, request, **kwargs):
        form = Contact
        return render(request, 'contact.html', {"form": form})

    def post(self, request, **kwargs):
        form = Contact(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ContactUs.objects.create(**data)
            return redirect('article:contact')


# --------------------------------------------------


class Posts(ListView):
    model = Article
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_posts'] = Article.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:4]
        return context


# -------------------------------------------------


class CategoryDetail(ListView):
    template_name = 'posts.html'
    paginate_by = 9
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category.Articles.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        context['popular_posts'] = Article.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:4]
        return context


# ----------------------------------------------------


class Search(ListView):
    model = Article
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            query_objects = Q()

            for word in query_list:
                query_objects |= Q(title__icontains=word)

            query_objects |= Q(title__iexact=query)

            return (Article.objects.annotate(match_count=Count('title', filter=query_objects))
                    .filter(match_count__gt=0)
                    .order_by('-match_count'))
        return Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_posts'] = Article.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:4]
        return context
