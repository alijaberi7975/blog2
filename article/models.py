# from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify
from mtranslate import translate

from account.models import User


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='  نام دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True, allow_unicode=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def save(self, *args, **kwargs):
        translation = translate(self.title, 'en')
        self.slug = slugify(translation, allow_unicode=True)
        super(Category, self).save(args, kwargs)


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, blank=True, related_name='Articles')
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to="image/article", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True, allow_unicode=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        translation = translate(self.title, 'en')
        self.slug = slugify(translation, allow_unicode=True)
        super(Article, self).save(args, kwargs)

    def get_absolute_url(self):
        return reverse('article:post', args=[self.slug])

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"


class AboutMe(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    description = models.TextField(verbose_name='توضیحات بیشتر')
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=13, verbose_name="تلفن")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='درباره من'
        verbose_name = "(درباره من)"


class ContactUs(models.Model):
    Name = models.CharField(max_length=30, verbose_name='نام')
    email = models.EmailField( verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    body = models.TextField( verbose_name='متن درخواست')
    created = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False, verbose_name='بررسی شده')

    def __str__(self):
        return f'{self.Name} , {self.phone}'

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = "تماس با ما"


class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    author = models.CharField(max_length=100)
    text = models.TextField()
    accept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} , {self.text}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user.full_name} - {self.article.title}'

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = "لایک ها"


class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='favorite')

    def __str__(self):
        return f'{self.user.full_name} - {self.article.title}'

    class Meta:
        verbose_name = 'مورد علاقه'
        verbose_name_plural = "مورد علاقه ها"