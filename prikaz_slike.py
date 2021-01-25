from PIL import Image as Im
from wand.image import Image

def odpri(datoteka):
    izhodna_datoteka = datoteka[:-4] + ".jpg"
    with Image(filename=datoteka) as f:
        f.format = 'jpeg'
        f.save(filename = izhodna_datoteka)
        slika = Im.open(izhodna_datoteka)
        slika.show()