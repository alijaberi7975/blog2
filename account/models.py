import time

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, full_name,  password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            full_name=full_name,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name,  password=None):
        user = self.create_user(email=email, full_name=full_name, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='ایمیل', max_length=255, unique=True)
    full_name = models.CharField(max_length=100, verbose_name='نام کامل')
    is_active = models.BooleanField(default=True, verbose_name='کاربر')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_writer = models.BooleanField(default=False, verbose_name='نویسنده')
    image = models.ImageField(upload_to="profile", null=True, blank=True,  verbose_name='تصویر نمایه')
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f'{self.full_name}({self.email})'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class RequestAnArticle(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده درخواست')
    request = models.TextField(verbose_name='متن درخواست')

    def __str__(self):
        return self.author.full_name

    class Meta:
        verbose_name = ' درخواست نوسیندگی'
        verbose_name_plural = " درخواست ها"