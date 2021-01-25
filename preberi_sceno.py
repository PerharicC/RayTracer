from raytracer import *
import json
s = """{"kamera": Kamera(Vektor(0,-0.3,-1), 1, 0.05),
	"širina":200,
	"višina": 200, 
	"predmeti": {"ravnina": Ravnina(Vektor(1, 0, 20), Vektor(0, 0, 3),1000, 1000, Material(Barva(1,0,1), Barva(0,0,0.02), Barva(1,1,1), 20,0)),
            	"krogla":Krogla(Vektor(0.75, -0.1, 1), 0.6, Material(Barva(1, 0, 0), Barva(0.01, 0, 0), Barva(0.1, 0.6, 0.6), 50, 0.4)),
            	"krogla2":Krogla(Vektor(-0.75, -0.1, 2.25), 0.6, Material(Barva(0, 1, 0), Barva(0.01, 0.01, 0.02), Barva(0.4, 1, 1), 20, 0.5)),
            	"krogla3":Krogla(Vektor(-0.75, 1000, 2.25), 999, Material(Barva(0.2, 0.2, 0.2), Barva(0.01, 0.01, 0.02), Barva(0, 0, 0), 0, 0.7)),
            	"valj": Valj(Vektor(0.75, -1, 1), Vektor(1, 1, 1), 0.5, 2, Material(Barva(1,1.,0.4), Barva(0.2,0.2,0.02), Barva(0.7,0.7,0.3), 50,0.4)),
            	"stozec": Stožec(Vektor(-0.85, -1, 1), Vektor(1,1,1), 0.5, 1, Material(Barva(0,0,1), Barva(0,0,0.02), Barva(1,1,1), 20,0.4))},
	"luci":{"luc": Točkasta_luč(Vektor(1.5, -10, -10),Material(Barva(1, 1, 1), Barva(0,0,0.0), Barva(1,1,1))),
        	"luc2": Točkasta_luč(Vektor(-0.5, -10.5, 5),Material(Barva(1, 1, 1), Barva(0,0,0.05), Barva(1,1,1)))}}"""
# def scena(f)
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

# a ="""{"kamera": {"pozicija":[0,-0.3,-1],"goriščna razdalja": 1, "zaslonka": 0.05},
# 	"širina": 200,
# 	"višina": 200, 
# 	"predmeti": {"ravnina1": {"normala" : [1, 0, 20], "pozicija": [0, 0, 3], "širina":1000,"višina": 1000, "material":{"barva":[1,0,1], "ambientalna barva": [0,0,0.02], "zrcaljenje":[1,1,1], "sijaj":20, "odsev":0}},
#             	"krogla1":{"središče": [0.75, -0.1, 1], "radij":0.6, "material":{"barva":[1, 0, 0], "ambientalna barva": [0.01, 0, 0], "zrcaljenje": [0.1, 0.6, 0.6], "sijaj":50, "odsev":0.4}},
#             	"krogla2":{"središče": [-0.75, -0.1, 2.25],"radij": 0.6, "material":{"barva":[0, 1, 0], "ambientalna barva":[0.01, 0.01, 0.02], "zrcaljenje":[0.4, 1, 1], "sijaj":20, "odsev":0.5}},
#             	"krogla3":{"središče": [-0.75, 1000, 2.25], "radij":999, "material":{"barva":[0.2, 0.2, 0.2], "ambientalna barva":[0.01, 0.01, 0.02],"zrcaljenje":[0, 0, 0], "sijaj":0, "odsev":0.7}},
#             	"valj1": {"pozicija":[0.75, -1, 1], "normala":[1, 1, 1], "radij":0.5, "višina":2, "material":{"barva":[1,1,0.4], "ambientalna barva": [0.2,0.2,0.02], "zrcaljenje":[0.7,0.7,0.3], "sijaj":50, "odsev":0.4}}},
#     "luči":{"luč1": {"pozicija":[1.5, -10, -10],"material":{"barva":[1, 1, 1], "zrcaljenje":[1,1,1]}},
#      	    "luč2": {"pozicija":[-0.5, -10.5, 5],"material":{"barva":[1, 1, 1], "ambientalna barva" : [0,0,0.05], "zrcaljenje":[1,1,1]}}},
# 	"število odbojev": 3}"""
# a = json.loads(a)
# print(a)
