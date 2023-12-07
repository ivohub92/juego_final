import random

class Nube:
    def __init__(self, pos, img, velocidad, profundidad):
        self.pos=list(pos)
        self.img= img
        self.velocidad= velocidad
        self.profundidad= profundidad

    def update(self):
        self.pos[0]+= self.velocidad

    def dibujar(self, superficie, offset=(0,0)):
        dibujo_pos=(self.pos[0]-offset[0]*self.profundidad,self.pos[1]-offset[1]*self.profundidad)
        superficie.blit(self.img, (dibujo_pos[0]%(superficie.get_width()+ self.img.get_width())-self.img.get_width(),dibujo_pos[1]%(superficie.get_height()+ self.img.get_height())-self.img.get_height()))

class Nubes:
    def __init__(self, nube_img, cantidad=16):
        self.nubes=[]
        for i in range(cantidad):
            self.nubes.append(Nube((random.random()*99999,random.random()*99999), random.choice(nube_img), random.random() *0.05 + 0.05, random.random()*0.6+0.2))
        
        self.nubes.sort(key=lambda x:x.profundidad) #llamo a sort, que ordena listas y sumo el argumento key
        #llamando a la funcion lambda, para pedirle que ordene por profundidad

    def update(self):
        for nube in self.nubes:
            nube.update()
    
    def dibujar(self, superficie, offset=(0,0)):
        for nube in self.nubes:
            nube.dibujar(superficie,offset)


