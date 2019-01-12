from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Textarea
from .models import Clanovi
from django.core.validators import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Lozinka', 'id': 'password'}))

    class Meta:
        model = User
        fields = ["username", 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': TextInput(attrs={'class': "form-control", 'placeholder': "Korisnicko ime"}),
            'first_name': TextInput(attrs={'class': "form-control", 'placeholder': "Ime"}),
            'last_name': TextInput(attrs={'class': "form-control", 'placeholder': "Prezime"}),
            'email': EmailInput(attrs={'class': "form-control", 'placeholder': "Email adresa"}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Nalog sa ovom email adresom vec postoji")
        return email

    def clean_first_name(self):
        ime = self.cleaned_data['first_name']
        return ime.title()

    def clean_last_name(self):
        prezime = self.cleaned_data['last_name']
        return prezime.title()


class ClanoviForma(forms.ModelForm):
    class Meta:
        model = Clanovi
        fields = ['profilna_slika', 'grad', 'omiljeni_sport', 'pol', 'broj_telefona', 'opis', 'instagram', 'twitter']
        widgets = {
            'grad': forms.Select(choices=Clanovi.gradovi, attrs={'class': 'form-control'}),
            'pol': forms.Select(choices=Clanovi.polovi, attrs={'class': 'form-control'}),
            'omiljeni_sport': forms.Select(choices=Clanovi.sportovi, attrs={'class': 'form-control'}),
            'broj_telefona': TextInput(attrs={'class': 'form-control', 'placeholder': "Broj telefona"}),
            'instagram': TextInput(attrs={'class': 'form-control', 'placeholder': "Instagram nalog"}),
            'twitter': TextInput(attrs={'class': 'form-control', 'placeholder': "Twitter nalog"}),
            'opis': Textarea(attrs={'class': 'form-control uredi_area', 'placeholder': 'Opis',}),

        }

    def clean_instagram(self):
        ime = self.cleaned_data['instagram']
        if ime:
            if ime[0] == '@':
                return ime[1:]
            else:
                return ime
        else:
            return ''

    def clean_twitter(self):
        ime = self.cleaned_data['twitter']
        if ime:
            if ime[0] == '@':
                return ime[1:]
            else:
                return ime
        else:
            return ''
