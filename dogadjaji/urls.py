from django.urls import path, include
from dogadjaji import views

app_name = 'dogadjaji'

urlpatterns = [
    path('novi_dogadjaj/', views.dodajDogadjaj, name='nov'),
    path('pretraga/', views.pretraga, name='pretraga'),
    path('prijava/<int:id_dog>', views.prijava, name='prijava'),
    path('moji_dogadjaji/', views.mojiDogadjaji, name='moji_dogadjaji'),
    path('prijava_rezultat/<int:prijava_id>', views.prijava_rezultat, name='prijava_rezultat'),
    path('kraj/<int:dogadjaj_kraj_id>/', views.kraj, name='kraj'),
    path('otkaz/<int:dogadjaj_za_otkaz>/', views.otkaz, name='otkaz'),
    path('ocenjivanje/<int:id_dog>/', views.ocenjuj, name='ocenjivanje'),
    path('ocena/<int:id_dog>/<int:usid>/', views.ocena, name='ocena'),
    path('<int:id_dog>/', views.pregled, name='pregled_dogadjaja'),
    path('izbaci/<int:id_dog>/<int:usid>/', views.izbaci, name='izbacivanje'),
    path('pozovi/<int:id_dog>/', views.pozovi, name='pozovi'),
    path('pozivi/', views.pozivi, name='pozivi'),

]
