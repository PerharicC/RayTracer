from raytracer import *

width = 200
height = 200
camera = Vektor(0,-0.3,-1)
predmeti_2={"valj": Valj(Vektor(-0.75, -0.3, 1), Vektor(1, 1, 1), 1, 1, Material(Barva(0,0,1), Barva(0,0,0.02), Barva(1,1,1), 20,0))}
predmeti = {
            "ravnina": Ravnina(Vektor(0, 0, 1), Vektor(0, 0, 3),1000, 1000, Material(Barva(0,0,1), Barva(0,0,0.02), Barva(1,1,1), 20,0)),
            "krogla":Krogla(Vektor(0.75, -0.1, 1), 0.6, Material(Barva(1, 0, 0), Barva(0.01, 0, 0), Barva(1, 1, 1), 50, 0.6)),
            "krogla2":Krogla(Vektor(-0.75, -0.1, 2.25), 0.6, Material(Barva(0, 1, 0), Barva(0.01, 0.01, 0.02), Barva(1, 1, 1), 20, 0.4)),
            "krogla3":Krogla(Vektor(-0.75, -1000, 2.25), 1000, Material(Barva(0.2, 0.2, 0.2), Barva(0.01, 0.01, 0.02), Barva(0, 0, 0), 0, 0.2)),
            "valj": Odprt_Valj(Vektor(0.75, -0.3, 1), Vektor(1, 1, 1), 1, 1, Material(Barva(0.6,0.4,0.4), Barva(0,0,0.02), Barva(1,1,1), 8,0.8))
            }
luči = {"luč": Točkasta_luč(Vektor(1.5, -0.5, -10),Material(Barva(1, 1, 1), Barva(0,0,0.05), Barva(1,1,1))),
        "luč2": Točkasta_luč(Vektor(-0.5, -10.5, 0),Material(Barva(1, 1, 1), Barva(0,0,0.05), Barva(1,1,1)))}
scene = Scena(camera, luči, predmeti_2,width, height)
rendaj = Render()
slika = rendaj.zrendaj(scene, 3)
ustvari_datoteko("test.ppm", scene, slika)
