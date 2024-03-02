"""
URL configuration for blog_02 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import PasswordResetForm
from django.urls import path, include
from django.contrib.auth import views as auth_views

# from account.models import User
# from django.contrib.auth.views import PasswordResetView
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext as _

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('account/', include('account.urls')),
                  path('', include('article.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# -----------------------------------------------------------------

# اینها ادرس ها و ویوهای و قالب های ریست پسورد پیشفرض جنگو هستن

#
# class CustomPasswordResetForm(PasswordResetForm):
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         # اعتبارسنجی اختصاصی شما را انجام دهید، برای مثال:
#         if not User.objects.filter(email=email).exists():
#             raise ValidationError("کاربری با این ایمیل در سایت ثبت نام نکرده لطفا ایمیل را درست وارد کنید.")
#         return email
#
#
# # در CustomPasswordResetView از این فرم اختصاصی استفاده کنید
# class CustomPasswordResetView(PasswordResetView):
#     form_class = CustomPasswordResetForm
#     template_name = "account/password_reset.html"
#
#     def form_valid(self, form):
#         # اگر ایمیل موجود بود، فرآیند بازیابی را ادامه دهید.
#         return super().form_valid(form)


urlpatterns += [
    path('password_reset', auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),
         name="password_reset"),
    path('password_reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('reset/done',
         auth_views.PasswordResetCompleteView.as_view(template_name="account/Password_reset_complete.html"),
         name="password_reset_complete"),
]
