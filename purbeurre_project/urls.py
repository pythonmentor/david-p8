"""purbeurre_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import PasswordsChangeView
from search import views
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    url(r"^$", views.index, name='index'),
    path("mentions/", include("search.urls")),
    url(r"^search/", include("search.urls")),
    url(r"^admin/", admin.site.urls),
    url(r"^register/$", views.register, name="register"),
    url(r"^accounts/", include("django.contrib.auth.urls"), name="login"),
    url(r"^password/", PasswordsChangeView.as_view(template_name="registration/change-password.html"), name='password'),
    url(r"^password_reset/", PasswordResetView.as_view(template_name='search/password_reset_form.html'), name='password_reset'),
    url(r"^password_reset/", PasswordResetDoneView.as_view(template_name='search/password_reset_done.html'), name='password_reset_done'),
    url(r"^password_reset/", PasswordResetConfirmView.as_view(template_name='search/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r"^password_reset/", PasswordResetCompleteView.as_view(template_name='search/password_reset_comlete.html'), name='password_reset_complete'),
    path('sentry-debug/', trigger_error),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns