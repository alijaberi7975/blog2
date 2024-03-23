from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from account.models import User, RequestAnArticle
from article.models import Article, Category

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.get(email=email)
        if user:
            raise ValidationError("کاربری با این ایمیل ثبت نام کرده است")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("رمزها با هم مطابقت ندارد")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'is_active', 'is_admin')


# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password']
#         widgets = {
#             "email": forms.EmailInput(
#                 attrs={"class": "form-control", "type": "text"}),
#             "password": forms.PasswordInput(
#                 attrs={"class": "form-control", "type": "password"}),
#         }
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if not User.objects.filter(email=email).exists():
#             raise forms.ValidationError('ایمیل وارد شده اشتباه است')
#         return email
#
#     def clean_password(self):
#         password = self.cleaned_data['password']
#         email = self.cleaned_data['email']
#         user = authenticate(email=email, password=password)
#         if user is None:
#             raise forms.ValidationError('رمز عبور وارد شده اشتباه است')
#         return password


class RegisterForm(forms.ModelForm):
    re_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "type": "password"}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 're_password']
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "type": "text"}),
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "type": "text"}),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "type": "password"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password and password != re_password:
            raise ValidationError("رمز عبور مطابقت ندارد")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("کاربری با این ایمیل ثبت نام کرده است")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError("پسورد حداقل باید از 8 کارکتر متشکل باشد")
        if not any(char.isupper() for char in password):
            raise ValidationError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد.')
        if not any(char.islower() for char in password):
            raise ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('رمز عبور باید حداقل یک عدد داشته باشد.')
        return password


# ---------------------------------------------------------------------------

class AddArticleForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Article
        fields = ['title', 'category', 'body', 'image']
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "type": "text", 'placeholder': 'عنوان'}),

            "body": forms.Textarea(
                attrs={"class": "form-control", "type": "Text", 'placeholder': 'متن مقاله'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise ValidationError('عنوان نمی‌تواند خالی باشد')
        existing_article = Article.objects.filter(title=title).first()
        if existing_article:
            raise ValidationError('مقاله ای در سایت با همین عنوان وجود دارد')
        return title


# -------------------------------------------------------------------------


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'full_name', 'image'}
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "type": "text",})
        }


# ------------------------------------------------------------------------


class EditArticleForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Article
        fields = ['title', 'category', 'body', 'image']
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "type": "text", "readonly": "readonly"}),

            "body": forms.Textarea(
                attrs={"class": "form-control", "type": "Text"}),
        }
