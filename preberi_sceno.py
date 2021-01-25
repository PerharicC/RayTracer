from raytracer import *
import json

def material(slovar):
    ključi_barv = ["barva", "ambientalna barva", "zrcaljenje"]
    ključi_koeficientov = ["sijaj", "odsev"]
    vrednosti = []
    for ključ in ključi_barv:
        if ključ not in slovar:
            vrednosti.append(Barva(0,0,0))
        else:
            vrednost = slovar[ključ]
            vrednosti.append(vnesi_podatke(vrednost, "barva"))
    for ključ in ključi_koeficientov:
        if ključ not in slovar:
            vrednosti.append(0)
        else:
            vrednosti.append(slovar[ključ])
    return vnesi_podatke(vrednosti, "material")

def vnesi_podatke(seznam, razred):
    if razred == "barva":
        return Barva(seznam[0], seznam[1], seznam[2])
    elif razred == "vektor":
        return Vektor(seznam[0], seznam[1], seznam[2])
    return Material(seznam[0], seznam[1], seznam[2], seznam[3], seznam[4])

def kamera(slovar):
    pozicija= slovar["pozicija"]
    pozicija = vnesi_podatke(pozicija, "vektor")
    return Kamera(pozicija, slovar["goriscna razdalja"], slovar["zaslonka"])

def luči(slovar):
    slovar_luči = {}
    for ime, tip in slovar.items():
        pozicija= tip["pozicija"]
        pozicija = vnesi_podatke(pozicija, "vektor")
        slovar_luči[ime] = Točkasta_luč(pozicija, material(tip["material"]))
    return slovar_luči

def predmeti(slovar):
    slovar_predmetov = {}
    for ime, predmet in slovar.items():
        if ime[:-1] == "ravnina":
            slovar_predmetov[ime] = ravnina(predmet)
        elif ime[:-1] == "krogla":
            slovar_predmetov[ime] = krogla(predmet)
        else:
            slovar_predmetov[ime] = valj(predmet, ime[:-1])
    return slovar_predmetov

def ravnina(slovar):
    pozicija = slovar["pozicija"]
    pozicija = vnesi_podatke(pozicija, "vektor")
    normala = slovar["normala"]
    normala = vnesi_podatke(normala, "vektor")
    return Ravnina(normala, pozicija, slovar["sirina"], slovar["visina"], material(slovar["material"]))

def krogla(slovar):
    središče = slovar["sredisce"]
    središče = vnesi_podatke(središče, "vektor")
    return Krogla(središče, slovar["radij"], material(slovar["material"]))

def valj(slovar, tip):
    pozicija = slovar["pozicija"]
    pozicija = vnesi_podatke(pozicija, "vektor")
    normala = slovar["normala"]
    normala = vnesi_podatke(normala, "vektor")
    if tip == "valj":
        return Valj(pozicija, normala, slovar["radij"], slovar["visina"], material(slovar["material"]))
    elif tip == "odprt valj":
        return Odprt_Valj(pozicija, normala, slovar["radij"], slovar["visina"], material(slovar["material"]))
    return Stožec(pozicija, normala, slovar["radij"], slovar["visina"], material(slovar["material"]))

def scena(datoteka):
    slovar = json.loads(open(datoteka, "r").read())
    kam = kamera(slovar["kamera"])
    objekti = predmeti(slovar["predmeti"])
    lučke = luči(slovar["luci"])
    return Scena(kam, lučke, objekti, slovar["sirina"], slovar["visina"]), slovar["stevilo odbojev"]
