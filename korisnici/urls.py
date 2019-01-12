from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "korisnici"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profil/', views.clanInfo, name='clanInfo'),
    path('login/', views.loginPage, name='loginPage'),
    path('podesavanja/', views.podesavanja, name='podesavanja'),
    path('lozinka/', views.promenaLozinke, name='lozinka'),
    path('pregled/<int:usid>', views.pregled, name='pregled'),

    ]


