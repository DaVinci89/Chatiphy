"""
URL configuration for Chatiphy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from post_maker.post_sitemaps import PostSitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'core.views.page_not_found'
handler400 = 'core.views.bad_request'
handler403 = 'core.views.forbidden'
handler500 = 'core.views.server_error'
handler503 = 'core.views.unavailable'

sitemaps = {
    'posts':PostSitemap,
}

urlpatterns = [
    path('', include("post_maker.urls", namespace="post_maker")),
    path('groups/', include("post_maker.urls", namespace="post_maker")),
    path('admin/', admin.site.urls),
    path('profile/', include("users.urls", namespace="users")),
    path("auth/", include("users.urls", namespace="users")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about/", include("about.urls", namespace="about")),
    path("sitemap.xml/", sitemap, {'sitemaps':sitemaps,}, name='django.contrib.sitemaps.views.sitemap'),
    path("api/v1/", include("post_maker.urls", namespace="post_maker")),
    path("api/v2/", include("users.urls", namespace="users"))

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
