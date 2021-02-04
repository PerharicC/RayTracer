import os
import sys
from raytracer import *
from prikaz_slike import odpri
from preberi_sceno import scena

datoteka_scena, datoteka_zapis = sys.argv[1:]
scene, odboj, AA = scena(datoteka_scena)
rendaj = Render()
slika = rendaj.zrendaj(scene, odboj)
ustvari_datoteko(datoteka_zapis, scene, slika, AA)
odpri(datoteka_zapis)
os.remove(datoteka_zapis)