from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from korisnici.models import Clanovi


# Create your models here.


class Dogadjaji(models.Model):
    TIME_ZONE = 'Europe/Belgrade'
    sportovi = (("Fudbal", "Fudbal"), ("Kosarka", "Kosarka"), ("Tenis", "Tenis"),
                ("Odbojka", "Odbojka"), ("Rukomet", "Rukomet"), ("Stoni tenis", "Stoni tenis"), ("Bilijar", "Bilijar"))
    novac = (("Nema nagrada", "Nema nagrada"), ("Ima nagrada", "Ima nagrada"))
    gradovi = (('Beograd', 'Beograd'), ('Valjevo', 'Valjevo'), ('Vranje', 'Vranje'), ('Zaječar', 'Zaječar'),
               ('Zrenjanin', 'Zrenjanin'), ('Jagodina', 'Jagodina'), ('Kragujevac', 'Kragujevac'),
               ('Kraljevo', 'Kraljevo'), ('Kruševac', 'Kruševac'), ('Leskovac', 'Leskovac'), ('Loznica', 'Loznica'),
               ('Niš', 'Niš'), ('Novi Pazar', 'Novi Pazar'), ('Novi Sad', 'Novi Sad'), ('Pančevo', 'Pančevo'),
               ('Požarevac', 'Požarevac'), ('Priština', 'Priština'), ('Smederevo', 'Smederevo'), ('Sombor', 'Sombor'),
               ('Sremska Mitrovica', 'Sremska Mitrovica'), ('Subotica', 'Subotica'), ('Užice', 'Užice'),
               ('Čačak', 'Čačak'), ('Šabac', 'Šabac'), ('Pirot', 'Pirot'))

    organizator = models.ForeignKey(Clanovi, on_delete=models.CASCADE, unique=False)
    datum_kreiranja = models.DateField(default=timezone.now)

    naziv = models.CharField(max_length=150, blank=False, null=False)
    datum_odrzavanja = models.DateField()
    opis = models.TextField(max_length=1000, blank=False, null=False)
    potrebno_igraca = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    novcana_nagrada = models.CharField(max_length=100, choices=novac, default="Nema novcane nagrade")
    novac_za_prijavu = models.PositiveIntegerField()
    grad = models.CharField(max_length=254, default="Nije naveden grad", choices=gradovi)
    mesto = models.CharField(max_length=150, blank=False)
    odrzano = models.BooleanField(default=False)
    sport = models.CharField(max_length=254, choices=sportovi, blank=False, null=False, default='Fudbal')
    ima_igraca = models.PositiveIntegerField(null=False, default=0)


class Prijava(models.Model):
    TIME_ZONE = 'Europe/Belgrade'

    status_prijave = (("Primljen", "Primljen"), ("Odbijen", "Odbijen"), ('Ceka se odgovor', 'Ceka se odgovor'))

    prijava_za_dogadjaj = models.ForeignKey(Dogadjaji, on_delete=models.CASCADE, unique=False)
    prijavu_poslao = models.ForeignKey(Clanovi, on_delete=models.CASCADE, unique=False)

    organizator = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)

    datum_prijave = models.DateField(default=timezone.now)

    primljen = models.CharField(max_length=100, default="Ceka se odgovor", choices=status_prijave)


class Ocenjivanje(models.Model):
    ocenio = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)

    koga_ocenio = models.ForeignKey(Clanovi, on_delete=models.CASCADE, unique=False)

    koji_dogadjaj = models.ForeignKey(Dogadjaji, on_delete=models.CASCADE, unique=False)

    ocena = models.FloatField(default=0)
    komentar = models.CharField(max_length=1000, blank=True, null=False, default="")
    datum_ocenjivanja = models.DateField(default=timezone.now)


class Glasao(models.Model):
    igrac = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    koji_dogadjaj = models.ForeignKey(Dogadjaji, on_delete=models.CASCADE, unique=False)
    zavrsio = models.BooleanField(default=False)


class Poziv(models.Model):
    status_prijave = (("Nije pogledano", "Nije pogledano"), ("Jeste pogledano", "Jeste pogledano"))
    pozvao = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    ko_je_pozvan = models.ForeignKey(Clanovi, on_delete=models.CASCADE, unique=False)
    koji_dogadjaj = models.ForeignKey(Dogadjaji, on_delete=models.CASCADE, unique=False)
    pogledano = models.CharField(max_length=100, default="Nije pogledano", choices=status_prijave)
    datum = models.DateField(default=timezone.now)
