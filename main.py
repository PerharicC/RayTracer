import os
from raytracer import *
from prikaz_slike import odpri
from preberi_sceno import scena

scene, odboj, AA = scena("scena_2.txt")
rendaj = Render()
slika = rendaj.zrendaj(scene, odboj)
ustvari_datoteko("test.ppm", scene, slika, AA)
odpri("test.ppm")
os.remove("test.ppm")