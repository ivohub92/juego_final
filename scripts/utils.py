import pygame
import os #gestion de archivos y directorios

BASE_IMG_PATH='data/imagenes/'

def obtener_fuente(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("data/menu/font.ttf", size)


def cargar_imagen(path):
    imagen= pygame.image.load(BASE_IMG_PATH + path).convert()
    imagen.set_colorkey((0,0,0))
    return imagen

#ordena la lista de nombres de archivos alfabéticamente .
def cargar_imagenes(path):
    imagenes= [] #lista vacia a cargar con imagenes
    for img_nombre in sorted(os.listdir(BASE_IMG_PATH + path)): #obtengo una lista de nombres de archivos en el directorio especificado.
        imagenes.append(cargar_imagen(path+ '/'+ img_nombre))
    return imagenes   

#IMG_DUR: cuantos frames queremos pasar por animacion
class Animacion:
    def __init__ (self, imagenes, img_dur=5, loop=True):
        self.imagenes=imagenes
        self.loop=loop
        self.img_dur= img_dur
        self.terminar= False
        self.frame= 0

    def copiar(self): 
        return Animacion(self.imagenes, self.img_dur, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.imagenes)) #devuelve elmodulo, generando un loop desde cero hasta un numero x
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.imagenes)-1) #elige entre dos valores, incrementando a self.frame 
            #hasta que llegue al valor que supere al otro y sale el minimo y se detiene
            if self.frame >= self.img_dur*len( self.imagenes)-1:
                self.terminar= True
    
    def img(self):        
        return self.imagenes[int(self.frame/self.img_dur)] #retorna el frame de animacion
    
     

    
    
