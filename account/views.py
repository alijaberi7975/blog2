from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from account.form import RegisterForm, AddArticleForm, EditProfileForm, EditArticleForm
from account.models import User, RequestAnArticle
from article.models import Article, FavoriteArticle


# -----------------------------------------------------------------------------


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('article:home')
        return render(request, "account/login.html", {'error_message': None})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('article:home')
        else:
            return render(request, "account/login.html", {'error_message': 'ایمیل یا رمز عبور اشتباه است'})


# ------------------------------------------------------------------------------------


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('article:home')


# -----------------------------------------------------------------------


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('article:home')
        form = RegisterForm()
        return render(request, "account/Register.html", context={"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            full_name = form.cleaned_data.get('full_name')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, full_name=full_name, password=password)
            return redirect('account:login')
        else:
            return render(request, "account/Register.html", context={"form": form})


# ----------------------------------------------------------------------------

#
# class PasswordResetView(PasswordResetView):
#     template_name = 'account/password_reset.html'
#     success_url = reverse_lazy('account:password_reset_done')
#
#
# class PasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'account/password_reset_done.html'
#     success_url = reverse_lazy('account:password_reset_done')
#
#
# class PasswordResetConfirmView(PasswordResetConfirmView):
#     success_url = '/account/password_reset_complete/'
#
#
# class PasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'your_custom_template/password_reset_complete.html'

# --------------------------------------------------------------------------------


class Profile(LoginRequiredMixin, View):
    def get(sel, request):
        user = request.user
        return render(request, 'account/Profile.html', {'user': user})


# -------------------------------------------------------------------------


class EditProfile(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = request.user
        form = EditProfileForm(instance=user)
        return render(request, 'account/Edit_Profie.html', {'form': form, 'user': user})

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
        else:
            form = EditProfileForm(instance=user)
            return render(request, 'account/Edit_Profie.html', {'form': form})


# --------------------------------------------------------------------------


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'account/Change_Password.html'
    success_url = reverse_lazy('account:profile')


# --------------------------------------------------------------------------------------


class AddArticle(LoginRequiredMixin, View):
    def get(self, request):
        form = AddArticleForm()
        return render(request, 'account/add_article.html', {'form': form})

    def post(self, request):
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            return redirect('account:user_article_list')
        return render(request, 'account/add_article.html', {'form': form})


# -------------------------------------------------------------------------------


class EditArticle(LoginRequiredMixin, View):
    def get(self, request, pk):
        article = Article.objects.filter(id=pk).first()
        if article and article.author == request.user:
            form = EditArticleForm(instance=article)
            return render(request, 'account/Edir_Article.html', {'form': form, 'article': article})
        else:
            return render(request, 'account/curbing.html')


def post(self, request, pk):
    article = get_object_or_404(Article, id=pk)
    form = EditArticleForm(request.POST, request.FILES, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.save()
        form.save()
        form.save_m2m()
        return redirect('account:user_article_list')
    else:
        form = EditArticleForm(request.POST, request.FILES, instance=article)
        return render(request, 'account/Edir_Article.html', {'form': form, 'article': article})


# ---------------------------------------------------------------------------------


class DeleteArticle(LoginRequiredMixin, View):
    def get(self, request, pk):
        article = Article.objects.filter(id=pk).first()
        if article and article.author == request.user:
            return render(request, 'account/Confrim_Delete_Article.html', {'article': article})
        else:
            return render(request, 'account/curbing.html')


def post(self, request, pk):
    article = Article.objects.get(id=pk)
    if 'confirm' in request.POST:
        article.delete()
        return redirect('account:user_article_list')
    elif 'cancel' in request.POST:
        return redirect('account:user_article_list')
    return redirect('account:user_article_list')


# -------------------------------------------------------------------


class UserArticleList(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'account/user_article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Articles'] = Article.objects.filter(author=self.request.user)
        return context


# -----------------------------------------------------------------


class FavoriteArticleList(LoginRequiredMixin, ListView):
    model = FavoriteArticle
    template_name = 'account/Favorite_article.html'
    context_object_name = 'favorite_articles'

    def get_queryset(self):
        return FavoriteArticle.objects.filter(user=self.request.user)


# ------------------------------------------------------------------------------


class EssayWriterForm(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'account/Essay_writer_form.html')

    def post(self, request):
        body = request.POST.get('request')
        if body:
            RequestAnArticle.objects.create(author=request.user, request=body)
            massage = 'درخواست شما با موفقیت ارسال شد و در دست بررسی می باشد'
            return render(request, 'account/Essay_writer_form.html', {'massage': massage})
        massage = 'متن درخواست را پر کنید'
        return render(request, 'account/Essay_writer_form.html', {'massage': massage})
