from django.shortcuts import render, redirect
from .models import Clanovi
from django.contrib import messages
from dogadjaji.models import Dogadjaji, Prijava, Glasao, Ocenjivanje

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User

from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import UserForm, ClanoviForma

from django.core.mail import send_mail
from django.template.loader import render_to_string


# Create your views here.


def index(request):
    poslato = False
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('korisnici:clanInfo'))
    else:
        if request.method == "POST":
            ime_prezime = request.POST["ime"]
            email = request.POST["email"]

            firma = request.POST["firma"]

            kontakt = request.POST["kontakt"]

            poruka = request.POST["poruka"]

            msg_plain = render_to_string('email.txt', {'ime_prezime': ime_prezime, "email": email, "firma": firma,
                                                       "kontakt": kontakt, "poruka": poruka})
            msg_html = render_to_string('email_firma.html',
                                        {'ime_prezime': ime_prezime, "email": email, "firma": firma, "kontakt": kontakt,
                                         "poruka": poruka})

            send_mail(
                'Firma zahtev',
                msg_plain,
                'markocar000@gmail.com',
                ['maksimovicm000@gmail.com'],
                html_message=msg_html,
            )
            poslato = True

        else:
            poslato = False

        return render(request, 'index.html', {"poslato": poslato})


def register(request):
    greske = False
    ispis = ""
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            napraviClana = Clanovi(user=user)
            napraviClana.save()
            login(request, user)
            return HttpResponseRedirect(reverse('korisnici:clanInfo'))
        else:
            print("\n\n\n Greska prilikom registracije \n\n " + str(user_form.errors) + "\n\n\n")
            greske = True
            ispis = str(user_form.errors)
            if "A user with that username already exists." in ispis:
                ispis = "Nalog sa ovim korisnickim imenov vec postoji"
            elif "Nalog sa ovom email adresom" in ispis:
                ispis = "Nalog sa ovom email adresom vec postoji"
            elif "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters" in ispis:
                ispis = "Korisnicko ime moze sadrzati samo slova, brojeve i karaktere: @/./+/-/_ "
            else:
                ispis = user_form.errors
    else:
        user_form = UserForm

    return render(request, "korisnici/registracija.html", context={"form": user_form, "greske": greske, "ispis": ispis})


def loginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('korisnici:clanInfo'))
    greska = False
    if request.method == "POST":
        username = request.POST.get('korisnicko_ime')
        password = request.POST.get("lozinka")

        print(username)
        print(password)

        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("korisnici:clanInfo"))
        else:
            greska = True
            print("\n\n\n")
            print("Greska prilikom unosa")
            print("\n\n\n")
            return render(request, 'korisnici/login.html', context={'greska': greska})

    else:
        return render(request, 'korisnici/login.html', context={'greska': greska})


@login_required
def clanInfo(request):
    user = request.user
    clan = Clanovi.objects.get(user=user)

    try:
        dal_glasao = Glasao.objects.filter(igrac=user, zavrsio=False)
    except Exception as e:
        dal_glasao = False
        print(e)
    rezultati_prijava = Prijava.objects.exclude(primljen="Ceka se odgovor").filter(
        prijavu_poslao=Clanovi.objects.get(user=user), prijava_za_dogadjaj__odrzano=False).exclude(
        organizator=user).order_by(
        'prijava_za_dogadjaj__datum_odrzavanja')
    ima = False
    if Dogadjaji.objects.filter(organizator=clan):
        ima = True
    print("\n\n\n")
    print(clan)
    print("\n\n\n")
    ocene_igraca = Ocenjivanje.objects.filter(koga_ocenio=clan, ocena__gt=0).order_by('-datum_ocenjivanja')
    lista_glasanja = []
    for ocena in ocene_igraca:
        if ocena.ocena <= 0 or ocena.ocena > 5:
            continue
        komentar = ocena.komentar
        lista_glasanja.append((Clanovi.objects.get(user=ocena.ocenio), ocena.ocena, komentar))
    print('\n\n\n')
    print(lista_glasanja)
    print('\n\n\n')
    return render(request, 'korisnici/clanInfo.html',
                  context={"user": user, "clan": clan, "ima": ima, 'prijave': rezultati_prijava,
                           'dal_glasao': dal_glasao, 'lista_glasanja': lista_glasanja})


@login_required
def promenaLozinke(request):
    promenjeno = 'ne'
    user = request.user
    clan = Clanovi.objects.get(user=user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            promenjeno = 'da'
            return render(request, 'korisnici/promenaLozinke.html',
                          {'form': form, 'clan': clan, 'user': user, 'promenjeno': promenjeno})
        else:
            promenjeno = 'greska'
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'korisnici/promenaLozinke.html',
                  {'form': form, 'clan': clan, 'user': user, 'promenjeno': promenjeno})


@login_required
def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def podesavanja(request):
    user = request.user
    clan = Clanovi.objects.get(user=user)
    greske = []
    if request.method == "POST":
        cl_form = ClanoviForma(data=request.POST, instance=clan)
        if cl_form.is_valid():
            cl_form.save(commit=True)
            if "profilna_slika" in request.FILES:
                print("\n\n\nIMA SLIKE\n\n\n")
                clan.profilna_slika = request.FILES['profilna_slika']
                clan.save()
        else:
            print("\n\n\nGRESKA")
            print(cl_form.errors)
            print("\n\n\n")

        return HttpResponseRedirect(reverse('korisnici:podesavanja'))


    else:
        cl_form = ClanoviForma
        return render(request, 'korisnici/podesavanja.html', context={"cl_form": cl_form, 'clan': clan})


@login_required
def pregled(request, usid):
    clan = Clanovi.objects.get(user_id=usid)
    user = User.objects.get(id=usid)
    print(clan.user.username)
    print(user.username)
    ocene_igraca = Ocenjivanje.objects.filter(koga_ocenio=clan, ocena__gt=0).order_by('datum_ocenjivanja')
    lista_glasanja = []
    for ocena in ocene_igraca:
        if ocena.ocena <= 0 or ocena.ocena > 5:
            continue
        komentar = ocena.komentar;
        lista_glasanja.append((Clanovi.objects.get(user=ocena.ocenio), ocena.ocena, komentar))

    return render(request, 'korisnici/pregled.html',
                  context={"user": user, "clan": clan, 'lista_glasanja': lista_glasanja})
