
from django.contrib import admin
from django.urls import path, include, re_path
from account.views import Login, logout_view

# path('blog/', include('blog.urls')),


urlpatterns = [
    path('', include('blog.urls')),
    path('logout/',logout_view, name='logout'),
    path('',include('django.contrib.auth.urls')),
    path("login/", Login.as_view(), name="login"),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('comment/', include('comment.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

