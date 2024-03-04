from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User, RequestAnArticle, VerificationCode
from account.form import UserChangeForm, UserCreationForm
from article.models import FavoriteArticle


class FavoriteArticleAdmin(admin.TabularInline):
    model = FavoriteArticle


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'full_name', 'is_admin', 'is_writer',)
    list_filter = ('is_admin', 'is_writer',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'image',)}),
        ('دسترسی ها', {'fields': ('is_admin', 'is_active', 'is_writer')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

admin.site.register(RequestAnArticle)

admin.site.register(VerificationCode)



