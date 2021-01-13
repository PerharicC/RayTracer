from math import sqrt
from numpy import linspace, array
from numpy.linalg import inv

class Vektor:

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "{0}, {1}, {2}".format(self.x, self.y, self.z)
    
    def __repr__(self):
        return "{0}, {1}, {2}".format(self.x, self.y, self.z)
    
    def skalarni_produkt(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def norma_vektorja(self):
        return sqrt(self.skalarni_produkt(self))
    
    def enotski_vektor(self):
        return self.množenje_s_skalarjem(1 / self.norma_vektorja())

    def vsota(self, other):
        return Vektor(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def razlika(self, other):
        return Vektor(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def množenje_s_skalarjem(self, skalar=1.0):
        return Vektor(skalar * self.x, skalar * self.y, skalar * self.z)
    
    def razdalja_med_krajevnima_vektorjema(self, other):
        d = self.razlika(other)
        return d.norma_vektorja()

    def razdalja_po_komponentah(self, other):
        return self.x - other.x, self.y - other.y, self.z - other.z
    
    def vektorski_produkt(self, other):
        return Vektor(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)


class Scena:

    def __init__(self, kamera, luči, predmeti, širina, višina):
        self.kamera = kamera
        self.luči = luči
        self.predmeti = predmeti
        self.širina = širina
        self.višina = višina

def vsi_piksli(širina, višina): #naredi matriko v velikosti zaslona
    piksli = []
    for j in range(višina):
        vrstica = []
        for i in range(širina):
            vrstica.append(None)
        piksli.append(vrstica)
    return piksli

class Barva:

    def __init__(self, R = 0.0, G = 0.0, B = 0.0):
        self.R = R
        self.G = G
        self.B = B
    
    def __str__(self):
        return "({0}, {1}, {2})".format(self.R, self.G, self.B)
    
    def __repr__(self):
        return "({0}, {1}, {2})".format(self.R, self.G, self.B)
    
    def naredi_piksel(self):

        def posamezna_barva(barva):
            if barva < 0.0:
                return 0
            elif barva > 1.0:
                return 1
            else:
                return barva
        
        rdeča, zelena, modra = posamezna_barva(self.R), posamezna_barva(self.G), posamezna_barva(self.B)
        return Barva(round(rdeča * 255), round(zelena* 255), round(modra * 255))
    
    def vsota_dveh_barv(self, other):
        return Barva(self.R + other.R, self.G + other.G, self.B + other.B)
    
    def množenje_barve(self, skalar=1.0):
        return Barva(self.R * skalar, self.G * skalar, self.B * skalar)
    
    def množenje_po_komponentah(self, other):
        return Barva(self.R * other.R, self.G * other.G, self.B * other.B)
    

def ustvari_datoteko(datoteka, scena, piksli):
    W = scena.širina
    H = scena.višina
    f = open(datoteka, "w")
    f.write("P3 {0} {1}\n255\n".format(W, H))
    for i in piksli:
        for j in i:
            piksel = j.naredi_piksel()
            f.write("{0} {1} {2} ".format(piksel.R, piksel.G, piksel.B))
        f.write("\n")
    f.close()


def kvadratna_enačba(a, b, c):
    Diskriminanta = b ** 2 - 4 * a * c
    if Diskriminanta > 0:
        x_1 = (- b + sqrt(Diskriminanta)) / (2 * a)
        x_2 = (- b - sqrt(Diskriminanta)) / (2 * a)
        if x_2 > 0:
            return x_2
        return x_1 if x_1 > 0 else None
    elif Diskriminanta == 0:
        x_1 = - b / (2 * a)
        return x_1 if x_1 > 0 else None
    return None

def kvadratna_enačba_za_valj(a, b, c):
    Diskriminanta = b ** 2 - 4 * a * c
    if Diskriminanta > 0:
        x_1 = (- b + sqrt(Diskriminanta)) / (2 * a)
        x_2 = (- b - sqrt(Diskriminanta)) / (2 * a)
        if x_2 > 0:
            return x_2, x_1
        elif x_1 > 0:
            return None, x_1
    elif Diskriminanta == 0:
        x_1 = - b / (2 * a)
        if x_1 > 0:
            return x_1, x_1
    return None, None

class Žarek:

    def __init__(self, kamera, točka):
        self.kamera = kamera
        self.točka = točka
    def __str__(self):
        return "Žarek z enačbo {} + {} * t".format(self.kamera, self.smerni_vektor())
    
    def smerni_vektor(self):
        smer = self.točka.razlika(self.kamera)
        return smer.enotski_vektor()
    
    def točka_na_žarku(self, skalar):
        smer = self.smerni_vektor()
        premik= smer.množenje_s_skalarjem(skalar)
        return self.kamera.vsota(premik)

class Krogla:

    def __init__(self, središče, radij, material):
        self.središče = središče
        self.radij = radij
        self.material = material
    
    def __str__(self):
        return "Krogla s središčem v S({}, {}, {}) in radijem {}".format(self.središče.x, self.središče.y, self.središče.z, self.radij)
    
    def zadetek(self, žarek):
        d = žarek.smerni_vektor()
        d_do_središča = žarek.kamera.razlika(self.središče)
        razdalja_do_središča = žarek.kamera.razdalja_med_krajevnima_vektorjema(self.središče)
        a = 1
        b = 2 * d.skalarni_produkt(d_do_središča)
        c = razdalja_do_središča ** 2 - self.radij ** 2
        return kvadratna_enačba(a, b, c)
    
    def normala(self, točka):
        return točka.razlika(self.središče).enotski_vektor()


class Render:
    
    def zrendaj(self, scena, število_odbojev=0):
        Kamera = scena.kamera
        W = scena.širina
        H = scena.višina
        razmerje_stranic = W / H
        zaslon = (-1.0, 1.0, -1/razmerje_stranic, 1/razmerje_stranic)
        X = linspace(-1, 1, W)
        Y = linspace(zaslon[2],zaslon[3], H)
        piksli = vsi_piksli(W, H)
        for j in range(len(Y)):
            y = Y[j]
            for i in range(len(X)):
                x = X[i]
                žarek = Žarek(kamera=Kamera, točka = Vektor(x, y))
                piksli[j][i] = self.poišči_predmet(žarek, scena, število_odbojev)
            print("{:3.0f}%".format(j * 100 /H), end="\r")
        return piksli
    
    def poišči_predmet(self, žarek, scena, število_odbojev): #Poišče najbližji predmet kameri in vrne njegovo barvo na tem mestu
        iskana_barva = Barva(0, 0, 0)
        razdalja_min = None
        predmet_min = None
        for predmet in scena.predmeti.values():
            if (type(predmet) is Valj) or (type(predmet) is Odprt_Valj):
                razdalja, normala_2 =predmet.zadetek(žarek)
            else:
                razdalja =  predmet.zadetek(žarek)
            if razdalja != None and (predmet_min == None or razdalja < razdalja_min):
                razdalja_min = razdalja
                predmet_min = predmet
        if predmet_min == None:
            return iskana_barva
        točka_zadetka =žarek.točka_na_žarku(razdalja_min)
        if type(predmet_min) is Krogla:
            normala = predmet_min.normala(točka_zadetka)
        elif type(predmet_min) is Ravnina:
            normala = predmet_min.normala
        else:
            normala = normala_2
        iskana_barva = self.poišči_barvo(predmet_min.material, točka_zadetka, normala, scena)
        odsev = predmet_min.material.odsev
        if število_odbojev == 0:
            return iskana_barva
        elif odsev == 0:
            return iskana_barva
        nova_točka = točka_zadetka.vsota(normala.množenje_s_skalarjem(0.001))
        nova_smer = žarek.smerni_vektor().razlika(normala.množenje_s_skalarjem(2 * normala.skalarni_produkt(žarek.smerni_vektor())))
        return iskana_barva.vsota_dveh_barv(self.poišči_predmet(Žarek(nova_točka, nova_točka.vsota(nova_smer)), scena, število_odbojev-1).množenje_barve(odsev))

    def poišči_barvo(self, material, vektor, normala, scena):
        ambientalna_barva = material.prostorska_osvetlitev
        barva = Barva(0,0,0)
        for luč in scena.luči.values():
            if type(luč) is Točkasta_luč:
                žarek_luč = Žarek(vektor,luč.točka)
            material_luči=luč.material
            ambient = ambientalna_barva.vsota_dveh_barv(material_luči.prostorska_osvetlitev)

            def barva_pri_osvetltivi(barva_predmeta, barva_luči, smer_luči, normala):
                skalarni = smer_luči.skalarni_produkt(normala)
                zmnožek_barv = barva_predmeta.množenje_po_komponentah(barva_luči)
                return Barva(0,0,0) if skalarni <=0 else zmnožek_barv.množenje_barve(skalarni)
            
            def barva_zrcaljenja(zrcaljenje_luči, zrcaljenje_predemta, smer_kamere, smer_luči, normala, sijaj):
                vektor = smer_kamere.vsota(smer_luči).enotski_vektor()
                skalarni = vektor.skalarni_produkt(normala)
                zmnožek_zrcaljenja = zrcaljenje_luči.množenje_po_komponentah(zrcaljenje_predemta)
                moč_osvetlitve = (skalarni ** (sijaj / 4))
                return Barva(0,0,0) if skalarni <=0 else zmnožek_zrcaljenja.množenje_barve(moč_osvetlitve)
            
            barva_osvetlite = barva_pri_osvetltivi(material.barva, material_luči.barva, žarek_luč.smerni_vektor(), normala)
            smer_kamere = Žarek(vektor, scena.kamera).smerni_vektor()
            barva_poudarka = barva_zrcaljenja(material_luči.zrcaljenje, material.zrcaljenje, smer_kamere, žarek_luč.smerni_vektor(), normala, material.koeficient_sijaja)
            barva = barva.vsota_dveh_barv(ambient).vsota_dveh_barv(barva_osvetlite).vsota_dveh_barv(barva_poudarka)
        return barva if len(scena.luči) != 0 else ambientalna_barva
    
            

class Ravnina:

    def __init__(self, normala, točka, širina, višina, material):
        self.normala = normala.enotski_vektor()
        self.točka = točka
        self.širina = širina
        self.višina = višina
        self.material = material
    
    def __str__(self):
        return "Ravnina z normalo ({}) in točko na ravnini({})".format(self.normala, self.točka)

    def vektorja_na_ravnini(self):
        #Vektor u
        d = self.normala.skalarni_produkt(self.točka)
        x, y, z = katero_komponento_si_zmisli(self.normala, d)
        u = Vektor(x, y, z).razlika(self.točka).enotski_vektor()
        #Vektor v
        v = self.normala.vektorski_produkt(u) #Ni treba normirati, ker sta a in n enotska ter pravokotna
        return u, v

    def zadetek(self, žarek):
        kamera, smer, normala, točka= žarek.kamera, žarek.smerni_vektor(), self.normala, self.točka
        širina, višina = self.širina, self.višina
        x = (točka.skalarni_produkt(normala) - kamera.skalarni_produkt(normala)) / smer.skalarni_produkt(normala)
        u, v = self.vektorja_na_ravnini()
        # max_dolžina = sqrt(2) * širina
        kje_je_žarek = žarek.točka_na_žarku(x)
        razdalja_do_središča = kje_je_žarek.razdalja_med_krajevnima_vektorjema(točka)
        projekcija_u = abs(kje_je_žarek.razlika(točka).skalarni_produkt(u))
        projekcija_v = abs(točka.razlika(kje_je_žarek).skalarni_produkt(v))
        if projekcija_u > širina / 2 or projekcija_v > višina / 2:
            return None
        return x
        # d = normala.skalarni_produkt(točka)
        # l = ((d - normala.y * (točka.y + točka.z * u.y / u.z)) / normala.x - točka.x - u.x * točka.z / u.z) / (v.y + u.x * v.z / u.z + normala.y / normala.x * (u.y * v.z / u.z +v.y))
        # k = - (točka.z + l * v.z) / u.z
        # if rezultat(kje_je_žarek, točka, u, v, širina, višina):
        #     print("yes")
        #     return x
        # if abs(l) /200 > višina / 2 or abs(k) /320 > širina / 2:
        #     print("haha")
        #     return None
        # return x
        # po_širini = linspace(-širina/2, širina/2, širina)
        # po_višini = linspace(-višina/2, višina/2, višina)
        # for i in po_širini:
        #     for j in po_višini:
        #         linearna_kombinacija = u.množenje_s_skalarjem(i).vsota(v.množenje_s_skalarjem(j))
        #         if linearna_kombinacija.razdalja_med_krajevnima_vektorjema(kje_je_žarek) < 0.1:
        #             print("yes")
        #         if linearna_kombinacija == žarek.točka:
        #             return x
        # return None

def katero_komponento_si_zmisli(normala, d):
            if normala.x != 0:
                y, z = (1, 1)
                x = (d - normala.y - normala.z) / normala.x
            elif normala.y != 0:
                x, z = (1, 1)
                y = (d - normala.x - normala.z) / normala.y
            else:
                x, y =(1, 1)
                z = (d - normala.x - normala.y) / normala.z
            return x, y, z

def rezultat(točka, središče, u, v, širina, višina):
    x, y, z = točka.razdalja_po_komponentah(središče)
    k = širina / 2
    l = višina / 2
    if abs((x - k * u.x) / v.x) > višina / 2:
        return None
    elif abs((y - k * u.y) / v.y) > višina / 2:
        return None
    elif abs((z - k * u.z) / v.z) > višina / 2:
        return None
    elif abs((x - l * v.x) / u.x) > širina / 2:
        return None
    elif abs((y - l * v.y) / u.y) > širina / 2:
        return None
    elif abs((z - l * v.z) / u.z) > širina / 2:
        return None
    else:
        return True


class Točkasta_luč:

    def __init__(self, točka, material):
        self.točka = točka
        self.material = material
    
    def __str__(self):
        return "Točkasta luč na mestu ({0}) z barvo ({1}).".format(self.točka, self.material.barva)
    
class Ravninska_luč:

    def __init__(self, ravnina, barva, moč=1.0):
        self.ravnina = ravnina
        self.barva = barva
        self.moč = moč
    
    def __str__(self):
        return "Ravninska luč na ravnini ({0}), z barvo ({1}) in {2} % močjo.".format(self.ravnina, self.barva, self.moč * 100)
    
class Material:

    def __init__(self, barva, prostorska_osvetlitev, zrcaljenje, koeficient_sijaja=0.0, odsev = 0.0):
        self.barva = barva
        self.prostorska_osvetlitev = prostorska_osvetlitev
        self.zrcaljenje = zrcaljenje
        self.koeficient_sijaja = koeficient_sijaja
        self.odsev = odsev

def množenje_matrik(A, B):
    B = [[B.x], [B.y], [B.z]]
    if len(A) == len(B):
        A_B = [ [ 0 for y in range(len(B[0])) ] 
                for x in range(len(A)) ]
        for i_1 in range(len(A)):
            for j_2 in range(len(B[0])):
                x = 0
                for k in range(len(A[0])):
                    x += A[i_1][k] * B[k][j_2]
                A_B[i_1][j_2] = x
        return Vektor(A_B[0][0], A_B[1][0], A_B[2][0])

def inverz(A): #inverz matrike A
    A=inv(array(A))
    B= []
    for vrstica in A:
        vrsta = []
        for element in vrstica:
            vrsta.append(element)
        B.append(vrsta)
    return B

class Valj:

    def __init__(self, točka, normala, radij, višina, material):
        self.točka = točka
        self.radij = radij
        self.višina = višina
        self.normala = normala.enotski_vektor()
        self.material = material
    
    def zadetek(self, žarek):
        kamera, smer, točka, višina, radij, normala = žarek.kamera, žarek.smerni_vektor(), self.točka, self.višina, self.radij, self.normala
        u, v = self.vektor_na_osnovni_ploskvi()
        prehod_B_S = [[u.x, v.x, normala.x], [u.y, v.y, normala.y], [u.z, v.z, normala.z]] #prehodna matrika iz baze {u, v, n} v standardno bazo
        prehod_S_B= inverz(prehod_B_S) #prehodna matrika iz standardne v novo bazo
        novo_središče = množenje_matrik(prehod_S_B, točka)
        središče=Vektor(novo_središče.x, novo_središče.y, 0)
        nova_smer=množenje_matrik(prehod_S_B, smer).enotski_vektor()
        smer=Vektor(nova_smer.x, nova_smer.y, 0)
        nova_kamera=množenje_matrik(prehod_S_B, kamera)
        kamera = Vektor(nova_kamera.x, nova_kamera.y)
        d_do_središča = kamera.razlika(središče)
        razdalja_do_središča = kamera.razdalja_med_krajevnima_vektorjema(središče)
        a = 1- nova_smer.z ** 2
        b = 2 * smer.skalarni_produkt(d_do_središča)
        c = razdalja_do_središča ** 2 - radij ** 2
        rezultat1=kvadratna_enačba(a, b, c)
        if rezultat1 is None:
            x, normala = self.osnovna_ploskev(novo_središče, nova_kamera, nova_smer)
            return x, normala
        elif (nova_kamera.z+nova_smer.z * rezultat1 < novo_središče.z) or (nova_kamera.z + nova_smer.z*rezultat1 > novo_središče.z + višina):
            x, normala = self.osnovna_ploskev(novo_središče, nova_kamera, nova_smer)
            return x, normala
        else:
            normala = self.normala_na_plašču(prehod_B_S, rezultat1, novo_središče, žarek)
            return rezultat1, normala
    
    def vektor_na_osnovni_ploskvi(self):
        d = self.normala.skalarni_produkt(self.točka)
        x, y, z = katero_komponento_si_zmisli(self.normala, d)
        u = Vektor(x, y, z).razlika(self.točka).enotski_vektor()
        v = self.normala.vektorski_produkt(u)
        return u, v
    
    def osnovna_ploskev(self, središče, kamera, smer):
        normala = Vektor(0,0,1)
        x = (središče.skalarni_produkt(normala) - kamera.skalarni_produkt(normala)) / smer.skalarni_produkt(normala)
        if (x > 0):
            točka_zadetka = kamera.vsota(smer.množenje_s_skalarjem(x))
            if kamera.z + smer.z * x == središče.z:
                if točka_zadetka.razdalja_med_krajevnima_vektorjema(središče) <= self.radij:
                    return x, self.normala.množenje_s_skalarjem(-1)
            elif kamera.z + smer.z * x == središče.z + self.višina:
                središče = Vektor(središče.x, središče.y, središče.z+self.višina)
                if točka_zadetka.razdalja_med_krajevnima_vektorjema(središče) <= self.radij:
                    return x, self.normala
        return None, None
    
    def normala_na_plašču(self, matrika, razdalja, središče, žarek):
        točka_zadetka = žarek.točka_na_žarku(razdalja)
        višinsko_središče = Vektor(središče.x, središče.y, točka_zadetka.z)
        normala = točka_zadetka.razlika(višinsko_središče)
        orig_normala = množenje_matrik(matrika, normala).enotski_vektor()
        return orig_normala

class Odprt_Valj(Valj):

    def zadetek(self, žarek):
        kamera, smer, točka, višina, radij, normala = žarek.kamera, žarek.smerni_vektor(), self.točka, self.višina, self.radij, self.normala
        u, v = self.vektor_na_osnovni_ploskvi()
        prehod_B_S = [[u.x, v.x, normala.x], [u.y, v.y, normala.y], [u.z, v.z, normala.z]]
        prehod_S_B= inverz(prehod_B_S)
        novo_središče = množenje_matrik(prehod_S_B, točka)
        središče=Vektor(novo_središče.x, novo_središče.y, 0)
        nova_smer=množenje_matrik(prehod_S_B, smer).enotski_vektor()
        smer=Vektor(nova_smer.x, nova_smer.y, 0)
        nova_kamera=množenje_matrik(prehod_S_B, kamera)
        kamera = Vektor(nova_kamera.x, nova_kamera.y)
        d_do_središča = kamera.razlika(središče)
        razdalja_do_središča = kamera.razdalja_med_krajevnima_vektorjema(središče)
        a = 1- nova_smer.z ** 2
        b = 2 * smer.skalarni_produkt(d_do_središča)
        c = razdalja_do_središča ** 2 - radij ** 2
        rezultat1, rezultat2=kvadratna_enačba_za_valj(a, b, c)
        if rezultat1 is None:
            if rezultat2 is None:
                return rezultat2, rezultat2
            elif (nova_kamera.z+nova_smer.z * rezultat2 < novo_središče.z) or (nova_kamera.z + nova_smer.z*rezultat2 > novo_središče.z + višina):
                return None,None
            normala = self.normala_na_plašču(prehod_B_S, rezultat2, novo_središče, žarek)
            return rezultat2, normala
        elif (nova_kamera.z+nova_smer.z * rezultat1 < novo_središče.z) or (nova_kamera.z + nova_smer.z*rezultat1 > novo_središče.z + višina):
            if (nova_kamera.z+nova_smer.z * rezultat2 < novo_središče.z) or (nova_kamera.z + nova_smer.z*rezultat2 > novo_središče.z + višina):
                return None,None
            normala = self.normala_na_plašču(prehod_B_S, rezultat2, središče, žarek)
            return rezultat2, normala
            
        else:
            normala = self.normala_na_plašču(prehod_B_S, rezultat1, novo_središče, žarek)
            return rezultat1, normala

    


    