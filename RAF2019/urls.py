"""RAF2019 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from korisnici import views

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('reset_lozinka/', auth_views.PasswordResetView.as_view(template_name='korisnici/reset.html'), name = 'password_reset'),
    path('reset_lozinka/kraj/', auth_views.PasswordResetView.as_view(template_name='korisnici/reset_potvrda.html'), name = 'password_reset_done'),
    path('reset_lozinka/potvrda/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='korisnici/resetuj.html'), name = 'password_reset_confirm'),
    path('reset_lozinka/zavrsio/', auth_views.PasswordResetCompleteView.as_view(template_name='korisnici/kraj.html'), name = 'password_reset_complete'),
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('korisnici/', include('korisnici.urls'), name="korisnici"),
    path('dogadjaji/', include('dogadjaji.urls'), name="dogadjaji"),
    path('logout/', views.logoutPage, name="logoutPage"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
