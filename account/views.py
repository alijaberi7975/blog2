from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from account.form import RegisterForm, AddArticleForm, EditProfileForm, EditArticleForm
from account.models import User, RequestAnArticle, VerificationCode
from article.models import Article, FavoriteArticle
from django.utils import timezone
from django.core.mail import send_mail
import random
import string


# -----------------------------------------------------------------------------


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('article:home')
        next_page = request.GET.get('next', '')
        return render(request, "account/login.html", {'error_message': None, 'next_page': next_page})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', '')
            return redirect(next_page or 'article:home')

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
            # ارسال ایمیل خوشامدگویی
            subject = 'خوش امد گویی به blog2'
            message = f"کاربر عزیز {full_name} به وبسایت ما خوش اومدی " \
                      f"اگر این ایمیل را دریافت کردی یعنی ثبت نام شما در سایت موفقیت امیز بوده و شما میتوانید با واردن شدن به حساب کاربری خود از امکانات سایت بهرمند بشید و به جدیدترین مقالات روز دنیا دسترسی داشته باشید " \
                      f"همچنین اگر شما در علاقه مند نوشتن مقالات هستید میتوانید از پروفایل کاربری خود درخواست مقاله نویسی بدهید تا کارشناسان ما بعد از بررسی درخواست شما دسترسی مقاله نوشتن را به شما بدهند " \
                      f"ممنون که ما را انتخاب کردید موفق باشد"
            from_email = 'alijaberi279@gmail.com'  # آدرس ایمیل خود را وارد کنید
            to_email = email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)
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
    def get(self, request):
        user = request.user
        form = EditProfileForm(instance=user)
        return render(request, 'account/Edit_Profile.html', {'form': form, 'user': user})

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
        else:
            form = EditProfileForm(instance=user)
            return render(request, 'account/Edit_Profile.html', {'form': form})


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
            return render(request, 'account/Inaccessibility.html')

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
            return render(request, 'account/Confirm_Delete_Article.html', {'article': article})
        else:
            return render(request, 'account/Inaccessibility.html')

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


# ------------------------------------------------


class DeleteAccount(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'account/Delete_User.html', {'user': user})

    def post(self, request):
        user = request.user
        if 'confirm' in request.POST:
            # تولید یک کد یکتا
            verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            # ایجاد توکن 20 کاراکتری یکتا
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            # حذف کدهای قدیمی‌تر از دیتابیس
            VerificationCode.objects.filter(expiration_time__lt=timezone.now()).delete()
            # ذخیره کد و توکن در مدل VerificationCode
            expiration_time = timezone.now() + timezone.timedelta(minutes=2)
            verification_obj = VerificationCode(user=user, code=verification_code, expiration_time=expiration_time,
                                                token=token)
            verification_obj.save()
            # ارسال کد تأیید از طریق ایمیل
            subject = 'کد تأیید حذف حساب کاربری'
            message = f'کاربر گرامی شما درخواست حذف حساب کاربری خود را داده اید' \
                      f'\n کد تائیدیه حذف حساب کاربری شما: {verification_code}'
            from_email = 'alijaberi279@gmail.com'  # آدرس ایمیل خود را وارد کنید
            to_email = user.email
            send_mail(subject, message, from_email, [to_email], fail_silently=False)

            massage = "کد تایید را به ایمیل شما ارسال کردیم لطفا در هنگام انجام عملیات صفحه را رفرش نکنید"
            return render(request, 'account/Confirm_Delete_User.html',
                          {'user': user, 'token': token, "massage": massage})

        elif 'remove' in request.POST:
            code = request.POST.get('verification_code')
            verification = VerificationCode.objects.filter(user=request.user, token=request.POST.get('token')).first()
            if code == verification.code:
                user.delete()
                verification.delete()
                return redirect('article:home')
            else:
                massage = "کد وارد شده اشتباه است "
                return render(request, 'account/Confirm_Delete_User.html',
                              {'user': user, 'token': verification.token, "massage": massage})

        elif 'cancel' in request.POST:
            return redirect("account:profile")

        return redirect("account:profile")
