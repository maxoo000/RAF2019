from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Clanovi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gradovi = (("Nije naveden grad", "Nije naveden grad"),
               ('Beograd', 'Beograd'), ('Valjevo', 'Valjevo'), ('Vranje', 'Vranje'), ('Zaječar', 'Zaječar'),
               ('Zrenjanin', 'Zrenjanin'), ('Jagodina', 'Jagodina'), ('Kragujevac', 'Kragujevac'),
               ('Kraljevo', 'Kraljevo'), ('Kruševac', 'Kruševac'), ('Leskovac', 'Leskovac'), ('Loznica', 'Loznica'),
               ('Niš', 'Niš'), ('Novi Pazar', 'Novi Pazar'), ('Novi Sad', 'Novi Sad'), ('Pančevo', 'Pančevo'),
               ('Požarevac', 'Požarevac'), ('Priština', 'Priština'), ('Smederevo', 'Smederevo'), ('Sombor', 'Sombor'),
               ('Sremska Mitrovica', 'Sremska Mitrovica'), ('Subotica', 'Subotica'), ('Užice', 'Užice'),
               ('Čačak', 'Čačak'), ('Šabac', 'Šabac'), ('Pirot', 'Pirot'))

    polovi = (("Musko", "Musko"), ("Zensko", "Zensko"), ("Bez navodjenja pola", "Bez navodjenja pola"))

    sportovi = (('Nije naveden omiljeni sport', "Nije naveden omiljeni sport"),
                ("Fudbal", "Fudbal"), ("Kosarka", "Kosarka"), ("Tenis", "Tenis"),
                ("Odbojka", "Odbojka"),("Rukomet","Rukomet"),("Stoni tenis","Stoni tenis"),("Bilijar","Bilijar"))

    profilna_slika = models.ImageField(default="profilne_slike/default.jpg", upload_to="profilne_slike")
    grad = models.CharField(max_length=254, default="Nije naveden grad", choices=gradovi)
    omiljeni_sport = models.CharField(max_length=254, choices=sportovi, default="Nije naveden omiljeni sport")
    pol = models.CharField(max_length=20, choices=polovi, default='Bez navodjenja pola')
    broj_telefona = models.CharField(max_length=35, default="Nije dodat broj telefona")
    opis = models.TextField(max_length=1000,blank=True, default="")
    prosecna_ocena = models.FloatField(default=0)
    instagram = models.CharField(max_length=150, default='', blank=True)
    twitter = models.CharField(max_length=150, default='', blank=True)
    firma = models.BooleanField(default=False, blank=True)

    def mailPregled(self):
        mail = self.user.email
        d = mail.split("@")
        if len(d[0])>3:
            return "***" + d[0][3:] + "@" + len(d[1].split(".")[0]) * "*" + '.' + d[1].split(".")[1]
        else:
            return mail
