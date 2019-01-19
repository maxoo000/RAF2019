from django.shortcuts import render

from .forms import df, Pretraga
from .models import Dogadjaji, Prijava, Ocenjivanje, Glasao, Poziv
from korisnici.models import Clanovi
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone


# Create your views here.
@login_required
def dodajDogadjaj(request):
    organizator = request.user
    clan = Clanovi.objects.get(user=organizator)
    ima = False
    if Dogadjaji.objects.filter(organizator=clan):
        ima = True
    if request.method == "POST":

        forma = df(data=request.POST)

        if forma.is_valid():
            naziv = forma.cleaned_data['naziv']
            mesto = forma.cleaned_data['mesto']
            opis = forma.cleaned_data['opis']
            datum_odrzavanja = forma.cleaned_data['datum_odrzavanja']
            novac_za_prijavu = forma.cleaned_data['novac_za_prijavu']
            potrebno_igraca = forma.cleaned_data['potrebno_igraca']
            grad = forma.cleaned_data['grad']
            sport = forma.cleaned_data['sport']
            novcana_nagrada = forma.cleaned_data['novcana_nagrada']
            dogadjaj = Dogadjaji(naziv=naziv, mesto=mesto, opis=opis, datum_odrzavanja=datum_odrzavanja,
                                 novac_za_prijavu=novac_za_prijavu, potrebno_igraca=potrebno_igraca,
                                 grad=grad, sport=sport, novcana_nagrada=novcana_nagrada, organizator=clan)
            dogadjaj.save()
            prijava_organizatora = Prijava(prijava_za_dogadjaj=dogadjaj, prijavu_poslao=clan, organizator=organizator,
                                           primljen="Primljen")
            prijava_organizatora.save()
            print('\n\n\nRADII\n\n\n')
        else:
            print("\n\n\nGRESKA")
            print(forma.errors)
            print("\n\n\n")

        return HttpResponseRedirect(reverse('korisnici:clanInfo'))

    else:
        forma = df
        return render(request, 'dogadjaji/nov_dogadjaj.html', context={"cl_form": forma})


@login_required
def pretraga(request):
    clan = Clanovi.objects.get(user=request.user)
    svi_dogadjaji = Dogadjaji.objects.all().exclude(organizator=clan).exclude(
        datum_odrzavanja__lt=timezone.now()).exclude()
    moje_prijave = Prijava.objects.filter(prijavu_poslao=clan)
    prijavio = []
    for jedna in moje_prijave:
        prijavio.append(jedna.prijava_za_dogadjaj_id)
    ima = False
    if Dogadjaji.objects.filter(organizator=clan):
        ima = True
    if request.method == 'POST':
        forma = Pretraga(request.POST)
        try:
            prosecna_ocena_pretrage = float(request.POST['rating'][:-1])
        except Exception as e:
            prosecna_ocena_pretrage = 0
            print(e)
        print("\n\n\n")
        print(prosecna_ocena_pretrage)
        print(type(prosecna_ocena_pretrage))
        print("\n\n\n")
        if forma.is_valid():
            grad = forma.cleaned_data['grad']
            sport = forma.cleaned_data['sport']
            ucesce = forma.cleaned_data['ucesce']
            nagrade = forma.cleaned_data['nagrade']
            potrebno_igraca = forma.cleaned_data['potrebno_igraca']
            trazi = True
            if ucesce == "Ne placa se ucesce":
                print('||||' + nagrade + "|||||||")
                if potrebno_igraca == 0:
                    print('igraca 0')
                    prikazani = svi_dogadjaji.filter(grad=grad, sport=sport, novac_za_prijavu=0,
                                                     novcana_nagrada=nagrade, odrzano=0,
                                                     organizator__prosecna_ocena__gte=prosecna_ocena_pretrage).exclude()

                else:
                    print('igraca 1')
                    prikazani = svi_dogadjaji.filter(grad=grad, sport=sport, potrebno_igraca=potrebno_igraca,
                                                     novcana_nagrada=nagrade, odrzano=0,
                                                     organizator__prosecna_ocena__gte=prosecna_ocena_pretrage)

            else:
                if potrebno_igraca == 0:
                    print("ima ucesca igraca 0")
                    prikazani = svi_dogadjaji.filter(grad=grad, sport=sport, novac_za_prijavu__gt=0,
                                                     novcana_nagrada=nagrade, odrzano=0,
                                                     organizator__prosecna_ocena__gte=prosecna_ocena_pretrage)
                else:
                    print('ima ucesca igraca 1')
                    prikazani = svi_dogadjaji.filter(grad=grad, sport=sport, novac_za_prijavu__gt=0,
                                                     novcana_nagrada=nagrade, odrzano=0,
                                                     potrebno_igraca=potrebno_igraca,
                                                     organizator__prosecna_ocena__gte=prosecna_ocena_pretrage)
        else:
            print(forma.errors)
            return HttpResponseRedirect(reverse('dogadjaji:pretraga'))
    else:
        trazi = False
        prikazani = svi_dogadjaji.filter(sport=clan.omiljeni_sport, grad=clan.grad,
                                         odrzano=0)
    forma = Pretraga
    print(prikazani)
    return render(request, 'dogadjaji/pretraga.html',
                  context={'trazi': trazi, 'prikazani': prikazani, 'forma': forma, "imaaa": ima, 'prijavio': prijavio})


@login_required
def prijava(request, id_dog):
    user = request.user
    clan = Clanovi.objects.get(user=user)

    dogadjaj = Dogadjaji.objects.get(id=id_dog)
    organizator = dogadjaj.organizator.user
    print(dogadjaj)
    print(clan.user.username)
    prijave_ovog_igraca = Prijava.objects.filter(prijavu_poslao=clan, prijava_za_dogadjaj=dogadjaj)
    if dogadjaj.ima_igraca >= dogadjaj.potrebno_igraca:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<br><br><br><br><h1 style='font-family:Arial;'><center>Maksimalan broj clanova je vec "
            "prijavljen na ovaj dogadjaj "
            "<br><br><small>Prozor ce se zatvoriti za 5 sekundi</small><center></h1>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    if prijave_ovog_igraca:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<br><br><br><br><h1 style='font-family:Arial;'><center>Vec ste se prijavili za ovaj "
            "dogadjaj<br><br><small>Prozor ce se zatvoriti za 5 sekundi</small><center></h1>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    if clan != dogadjaj.organizator:
        prijava = Prijava(prijavu_poslao=clan, prijava_za_dogadjaj=dogadjaj, organizator=organizator)
        prijava.save()
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<br><br><br><br><h1 style='font-family:Arial;'><center>Prijava uspesno poslata."
            " Mozete zatvoriti ovu stranicu.<br><br><small>Prozor ce se zatvoriti za 5 sekundi</small></center></h1>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    else:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<br><br><br><br><h1 style='font-family:Arial;'><center>Ne mozete da se prijavite na svoj turnir."
            "<br><br><small>Prozor ce se zatvoriti za 5 sekundi</small></center></h1>"
            "<script>setTimeout(function(){window.close();},5000);</script>")


@login_required
def mojiDogadjaji(request):
    user = request.user
    clan = Clanovi.objects.get(user=user)
    moji_dogadjaji = Dogadjaji.objects.filter(organizator=clan, odrzano=0)
    moje_prijave_cekanje = Prijava.objects.filter(organizator=user, primljen="Ceka se odgovor")
    print(moje_prijave_cekanje)
    return render(request, 'dogadjaji/moji_dogadjaji.html',
                  context={'user': user, 'clan': clan, 'moji_dogadjaji': moji_dogadjaji, 'ceka': moje_prijave_cekanje})


@login_required
def prijava_rezultat(request, prijava_id):
    user = request.user
    if request.method == "POST":
        prijava_poslata = Prijava.objects.get(id=prijava_id)
        za_dogadjaj = Dogadjaji.objects.get(id=prijava_poslata.prijava_za_dogadjaj.id)
        print(za_dogadjaj)
        prijavu_poslao_clan = prijava_poslata.prijavu_poslao
        prijava_poslata_user = prijavu_poslao_clan.user
        if za_dogadjaj.potrebno_igraca == za_dogadjaj.ima_igraca:
            return HttpResponse("Dogadjaj je vec popunjen")
        if prijava_poslata.prijavu_poslao == user:
            return HttpResponse("Ne mozete se prijaviti na svoj turnir")
        else:
            if prijava_poslata.prijava_za_dogadjaj.odrzano == 1:
                return HttpResponse("Ovaj dogadjaj je vec zavrsen")
            else:
                if prijava_poslata.primljen == "Primljen":
                    return HttpResponse("Igrac je vec primljen na dogadjaj")
                elif prijava_poslata.primljen == "Odbijen":
                    return HttpResponse("Igrac je vec odbijen sa turnira")
                else:
                    if request.POST['izbor'] == "prihvati":

                        prijava_poslata.primljen = "Primljen"
                        prijava_poslata.save()
                        za_dogadjaj.ima_igraca += 1
                        za_dogadjaj.save()
                        print("\n\n\nPrimljen\n\n\n")
                        return HttpResponseRedirect(reverse("dogadjaji:moji_dogadjaji"))
                    else:
                        prijava_poslata.primljen = "Odbijen"
                        prijava_poslata.save()
                        print("\n\n\nPrimljen\n\n\n")
                        return HttpResponseRedirect(reverse("dogadjaji:moji_dogadjaji"))


    else:
        return HttpResponseRedirect(reverse("dogadjaji:moji_dogadjaji"))


@login_required
def kraj(request, dogadjaj_kraj_id):
    user = request.user
    clan = Clanovi.objects.get(user=user)

    dogadjaj = Dogadjaji.objects.get(id=dogadjaj_kraj_id)
    prijave_za_dogadjaj = Prijava.objects.filter(primljen="Primljen", prijava_za_dogadjaj=dogadjaj)
    if dogadjaj.organizator != clan:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Vi niste organizator ovog dogadjaja"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    else:
        if dogadjaj.datum_odrzavanja > timezone.now().date():
            print("Datum odrzavanja dogadjaja jos nije prosao")
            return render(request, "dogadjaji/zavrsen.html", context={"datum": dogadjaj.datum_odrzavanja})

        else:
            if dogadjaj.ima_igraca == 0:
                return HttpResponse(
                    "<head><title>MAXO</title></head>"
                    "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Nije moguce zavrsiti dogadjaj sa 0 "
                    "clanova</h1>"
                    "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
                    "<script>setTimeout(function(){window.close();},5000);</script>")
            else:
                dogadjaj.odrzano = True
                dogadjaj.save()
                for igrac in prijave_za_dogadjaj:
                    nov_glas = Glasao(igrac=igrac.prijavu_poslao.user, koji_dogadjaj=dogadjaj)
                    nov_glas.save()
                prijavljeni = Prijava.objects.filter(primljen="Primljen", prijava_za_dogadjaj=dogadjaj)
                for ocenjuje in prijavljeni:
                    for ocenjivan in prijavljeni:
                        if ocenjuje != ocenjivan:
                            nova_ocena = Ocenjivanje(ocenio=ocenjuje.prijavu_poslao.user,
                                                     koga_ocenio=ocenjivan.prijavu_poslao, koji_dogadjaj=dogadjaj)
                            nova_ocena.save()
                        else:
                            pass

                return HttpResponse(
                    "<head><title>MAXO</title></head>"
                    "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Dogadjaj je uspesno zavrsen</h1>"
                    "<br><h3>Obavestenje za glasanje je poslato ucesnicima</h3>"
                    "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
                    "<script>setTimeout(function(){window.close();},5000);</script>")


@login_required
def otkaz(request, dogadjaj_za_otkaz):
    user = request.user
    clan = Clanovi.objects.get(user=user)

    dogadjaj = Dogadjaji.objects.get(id=dogadjaj_za_otkaz)
    if dogadjaj.organizator != clan:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Vi niste organizator ovog dogadjaja"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    else:
        dogadjaj.delete()
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Uspesno ste obrisali svoj dogadjaj</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")


@login_required
def ocenjuj(request, id_dog):
    user = request.user
    clan = Clanovi.objects.get(user=user)
    koji_dogadjaj = Dogadjaji.objects.get(id=id_dog)
    try:
        moja_prijava = Prijava.objects.get(prijavu_poslao=clan, prijava_za_dogadjaj=koji_dogadjaj)
        if moja_prijava.primljen != "Primljen":
            return HttpResponse(
                "<head><title>MAXO</title></head>"
                "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Ne mozete da glasate za ovaj"
                " dogadjaj posto niste primljeni</h1>"
                "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
                "<script>setTimeout(function(){window.close();},5000);</script>")
    except:
        pass

    if koji_dogadjaj.odrzano == False:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Ovaj dogadjaj jos nije zavrsen</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    try:
        if Glasao.objects.get(igrac=user, koji_dogadjaj=koji_dogadjaj).zavrsio:
            return HttpResponse(
                "<head><title>MAXO</title></head>"
                "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Zavrsili ste sa glasanjem za ovaj dogadjaj</h1>"
                "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
                "<script>setTimeout(function(){window.close();},5000);</script>")
    except:
        pass
    igraci_za_glasanje = Ocenjivanje.objects.filter(ocenio=user, koji_dogadjaj=koji_dogadjaj, ocena__exact=0)
    try:
        igrac = igraci_za_glasanje[0]

        # Staviti kada se na stranici posalje glas da ode na url koji cu da napravim i da se tu glas obradi i
        # posle izmeniti ovo za filter nekako da ako je vec glasano za tog igraca da vise ne glasa
    except:

        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Doslo je do greske</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    return render(request, 'dogadjaji/ocenjivanje.html', context={'igrac': igrac})


@login_required
def ocena(request, id_dog, usid):
    # print(usid)
    # print(id_dog)
    user = request.user
    clan = Clanovi.objects.get(user=user)
    koji_dogadjaj = Dogadjaji.objects.get(id=id_dog)
    try:
        dal_moze = Prijava.objects.get(prijavu_poslao=clan, prijava_za_dogadjaj=koji_dogadjaj, primljen="Primljen")
        print("\n\n\n", dal_moze)
        if dal_moze:
            print(dal_moze)
        else:
            print("GRESKA")
            return HttpResponse(
                "<head><title>MAXO</title></head>"
                "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Doslo je do greske</h1>"
                "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
                "<script>setTimeout(function(){window.close();},5000);</script>")
    except Exception as e:
        print("NE MOZETE GLASATI\n\n\n\n", e)
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Vi ne mozete glasati</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    ocenjuje_igraca = User.objects.get(id=usid)
    print(ocenjuje_igraca)
    clan_ocenjen = Clanovi.objects.get(user=ocenjuje_igraca)
    provera = Ocenjivanje.objects.get(ocenio=user, koga_ocenio=clan_ocenjen, koji_dogadjaj=koji_dogadjaj)
    if provera.ocena > 0:
        print("Vec ste ocenili ovog igraca")
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Vec ste glasali za ovog igraca</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    try:
        ocena = float(request.POST['rating'][:-1])
    except:
        ocena = 0
    try:
        komentar = str(request.POST['komentar']).strip()
    except:
        komentar = ""
    nova_ocena = Ocenjivanje.objects.get(ocenio=user, koga_ocenio=clan_ocenjen, koji_dogadjaj=koji_dogadjaj)
    nova_ocena.ocena = ocena
    nova_ocena.komentar = komentar
    nova_ocena.save()
    igraci_za_glasanje = Ocenjivanje.objects.filter(ocenio=user, koji_dogadjaj=koji_dogadjaj, ocena__exact=0)
    if igraci_za_glasanje:
        print("\n\n\n")
        print(igraci_za_glasanje)
        ocene_igraca = Ocenjivanje.objects.filter(koga_ocenio=clan_ocenjen)
        zbir = 0
        ocene = 0
        for jedna in ocene_igraca:
            if jedna.ocena <= 0.1 or jedna.ocena > 5:
                continue
            zbir += jedna.ocena
            ocene += 1
        prosek = zbir / ocene
        clan_ocenjen.prosecna_ocena = prosek
        clan_ocenjen.save()
        url = reverse('dogadjaji:ocenjivanje', kwargs={'id_dog': koji_dogadjaj.id})
        return HttpResponseRedirect(url)
    else:
        glas = Glasao.objects.get(igrac=user, koji_dogadjaj=koji_dogadjaj)
        glas.zavrsio = True
        glas.save()
        ocene_igraca = Ocenjivanje.objects.filter(koga_ocenio=clan_ocenjen)
        zbir = 0
        ocene = 0
        for jedna in ocene_igraca:
            if jedna.ocena <= 0.1 or jedna.ocena > 5:
                continue
            zbir += jedna.ocena
            ocene += 1
        prosek = zbir / ocene
        clan_ocenjen.prosecna_ocena = prosek
        clan_ocenjen.save()
        return HttpResponseRedirect(reverse('korisnici:clanInfo'))


@login_required
def pregled(request, id_dog):
    user = request.user
    clan = Clanovi.objects.get(user=user)

    dogadjaj = Dogadjaji.objects.get(id=id_dog)

    organizator = dogadjaj.organizator
    prijavljeni = Prijava.objects.filter(prijava_za_dogadjaj=dogadjaj, primljen="Primljen")
    if organizator == clan:
        editor = True
        prijavio = True
    else:
        editor = False
        svi_prijavljeni = Prijava.objects.filter(prijava_za_dogadjaj=dogadjaj)
        prijavljeni_clanovi = []

        for jedan in svi_prijavljeni:
            prijavljeni_clanovi.append(jedan.prijavu_poslao)
        if clan in prijavljeni_clanovi:
            prijavio = True
        else:
            prijavio = False

        print(prijavio)
    # ZAVRSITI PRIKAZ DOGADJAJA I URADITI IZBACIVANJE IGRACA AKO JE USER ORGANIZATOR
    print(editor)
    return render(request, 'dogadjaji/dogadjaj.html',
                  {"editor": editor, "dogadjaj": dogadjaj, "prijavljeni": prijavljeni, "prijavio": prijavio})


@login_required
def izbaci(request, id_dog, usid):
    user = request.user
    clan = Clanovi.objects.get(user=user)
    try:
        user_za_izbacivanje = User.objects.get(id=usid)
    except:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Korisnik kojeg zelite da izbacite ne postoji</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    try:

        dogadjaj = Dogadjaji.objects.get(id=id_dog)

    except:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Dogadjaj ne postoji</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    clan_za_izbacivanje = Clanovi.objects.get(user=user_za_izbacivanje)
    prijavljeni = Prijava.objects.get(prijava_za_dogadjaj=dogadjaj, prijavu_poslao=clan_za_izbacivanje)

    if user_za_izbacivanje == user:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Ne mozete izbaciti samog sebe</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    if prijavljeni.primljen != "Primljen":
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Igrac nije primljen na ovaj dogadjaj</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    if dogadjaj.odrzano == True:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Ovaj dogadjaj je vec zavrsen</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    prijavljeni.primljen = "Odbijen"
    prijavljeni.save()
    dogadjaj.ima_igraca -= 1
    dogadjaj.save()
    return HttpResponse(
        "<head><title>MAXO</title></head>"
        "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Igrac je uspesno uklonjen sa dogadjaja</h1>"
        "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
        "<script>setTimeout(function(){window.close();},5000);</script>")


@login_required
def pozovi(request, id_dog):
    if request.method != "POST":
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Doslo je do greske</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    usid = str(request.POST['username']).strip()

    user = request.user
    clan = Clanovi.objects.get(user=user)

    try:
        user_za_poziv = User.objects.get(username=usid)
        clan_za_poziv = Clanovi.objects.get(user=user_za_poziv)
    except:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Ovaj korisnik ne postoji</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    if user == user_za_poziv:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Ne mozete pozvati samog sebe</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    try:
        dogadjaj = Dogadjaji.objects.get(id=id_dog)
    except:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Dogadjaj ne postoji</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    if dogadjaj.odrzano == True:
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Dogadjaj je vec odrzan</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")

    try:
        pozivi = Poziv.objects.get(pozvao=user, ko_je_pozvan=clan_za_poziv, koji_dogadjaj=dogadjaj)
        return HttpResponse(
            "<head><title>MAXO</title></head>"
            "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Vec ste pozvali ovog igraca na ovaj dogadjaj</h1>"
            "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
            "<script>setTimeout(function(){window.close();},5000);</script>")
    # ZAVRSITI POZIVANJE
    # SMISLITI KAKO DA AKO VISE LJUDI POZOVE NA JEDAN DOGADJAJ DA TO BUDE PRIKAZANO NEKAKO DRUGACIJE
    except:
        try:
            prijava = Prijava.objects.get(prijava_za_dogadjaj=dogadjaj, prijavu_poslao=clan_za_poziv)
            return HttpResponse(
                "<head><title>MAXO</title></head>"
                "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Igrac je vec poslao prijavu za ovaj dogadjaj</h1>"
                "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
                "<script>setTimeout(function(){window.close();},5000);</script>")
        except:
            pozivi = Poziv(pozvao=user, ko_je_pozvan=clan_za_poziv, koji_dogadjaj=dogadjaj)
            pozivi.save()
            return HttpResponse(
                "<head><title>MAXO</title></head>"
                "<center><h1 style='font-family:Arial; margin-top: 20vh;'>Poziv za ucesce je poslat</h1>"
                "<br>Stranica ce se zatvoriti za 5 sekundi</center>"
                "<script>setTimeout(function(){window.close();},5000);</script>")


@login_required
def pozivi(request):
    user = request.user
    clan = Clanovi.objects.get(user=user)
    pozivi = Poziv.objects.filter(ko_je_pozvan=clan).order_by('-id')
    for poziv in pozivi:
        if poziv.pogledano == "Jeste pogledano":
            continue
        poziv.pogledano = "Jeste pogledano"
        poziv.save()
    print(pozivi)

    return render(request, 'dogadjaji/pozivi.html', {"pozivi": pozivi})


