from django.contrib.auth import views
from django.urls import path
from .views import (home,
                    user_signup,
                    users_list,
                    ArticleList,
                    ArticleCreate,
                    ArticleUpdate,
                    ArticleDelete,
                    Profile,
                )

app_name = 'account'


urlpatterns = [
    path('',ArticleList.as_view(), name = 'home'),
    path('article/create/',ArticleCreate.as_view(), name='article-create'),
    path('article/update/<int:pk>',ArticleUpdate.as_view(), name='article-update'),
    path('article/Delete/<int:pk>',ArticleDelete.as_view(), name='article-delete'),
    path('profile/',Profile.as_view(), name='profile'),
    path('create-account/', user_signup, name='create-account'),
    path('users/',users_list, name = 'users-list')
]