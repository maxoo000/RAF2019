from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, Textarea
from .models import Dogadjaji, Prijava
from django.core.validators import ValidationError

gradovi = Dogadjaji.gradovi
sportovi = Dogadjaji.sportovi
nagrade = (("Nema nagrada", "Nema nagrada"), ("Ima nagrada", "Ima nagrada"))
ucesce = (("Ne placa se ucesce", "Ne placa se ucesce"), ("Place se ucesce", "Placa se ucesce"))


class df(forms.Form):
    naziv = forms.CharField(max_length=125,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Naziv dogadjaja'}))
    mesto = forms.CharField(max_length=125, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mesto odrzavanja dogadjaja'}))
    opis = forms.CharField(max_length=1000,
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Opis dogadjaja'}))
    datum_odrzavanja = forms.CharField(max_length=125,
                                       widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))
    novac_za_prijavu = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": 'form-control', 'value': 0, 'step': '100'}))
    potrebno_igraca = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": 'form-control', 'value': 1, 'min': 1}))
    grad = forms.ChoiceField(choices=Dogadjaji.gradovi, widget=forms.Select(attrs={'class': 'form-control'}))
    sport = forms.ChoiceField(choices=Dogadjaji.sportovi, widget=forms.Select(attrs={'class': 'form-control'}))
    novcana_nagrada = forms.ChoiceField(choices=Dogadjaji.novac, widget=forms.Select(attrs={'class': 'form-control'}))


class Pretraga(forms.Form):
    grad = forms.ChoiceField(choices=gradovi, widget=forms.Select(attrs={'class': 'form-control'}))
    sport = forms.ChoiceField(choices=sportovi, widget=forms.Select(attrs={'class': 'form-control'}))
    nagrade = forms.ChoiceField(choices=nagrade, widget=forms.Select(attrs={'class': 'form-control'}))
    ucesce = forms.ChoiceField(choices=ucesce, widget=forms.Select(attrs={'class': 'form-control'}))
    potrebno_igraca = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": 'form-control', 'value': 0, 'min': 0}))
