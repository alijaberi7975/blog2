from django.urls import path
from account.views import LoginView, LogoutView, RegisterView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, Profile, AddArticle, UserArticleList, EssayWriterForm, \
    EditArticle, DeleteArticle, EditProfile, PasswordChange, FavoriteArticleList, DeleteAccount
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),

    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile', Profile.as_view(), name='profile'),
    path('addarticle', AddArticle.as_view(), name='add_article'),
    path('userarticelist', UserArticleList.as_view(), name='user_article_list'),
    path('EssayWriter', EssayWriterForm.as_view(), name='EssayWriter'),
    path('editarticle/<int:pk>', EditArticle.as_view(), name='edit_article'),
    path('deletearticle/<int:pk>', DeleteArticle.as_view(), name='delete_article'),
    path('editprofile', EditProfile.as_view(), name='edit_profile'),
    path('change_password', PasswordChange.as_view(), name='change_password'),
    path('favoritearticle', FavoriteArticleList.as_view(), name='favorite_article'),
    path('deleteaccount', DeleteAccount.as_view(), name='delete_account'),
]
