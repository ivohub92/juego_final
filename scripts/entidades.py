import pygame
import random

class Entidadesfisicas:
    def __init__(self,juego, tipo, pos, tamano):
        self.juego= juego
        self.tipo= tipo
        self.pos= list(pos) #paso esto a lista porque asi cada entidad tiene su lista. esta lista de posicion puede variar or eso no uso tupla
        self.tamano=tamano
        self.velocidad= [0,0] 
        self.colision = {'up': False, 'down': False, 'right': False, 'left': False}#chequeamos tipos de colisiones que tenemos
        self.accion= ''
        self.anim_offset= (-4,-2)#corregimos los errores de dimension de los distintos frames
        self.rotar=False
        self.accion_actual('quieto') 
        self.score=0

    def rect(self):        
        return pygame.Rect(self.pos[0], self.pos[1], self.tamano[0], self.tamano[1])

    def accion_actual(self, accion):
        if accion!= self.accion:
            self.accion=accion
            self.animacion= self.juego.assets[self.tipo + '/' + self.accion].copiar()#llamo a la animacion y pasan las posiciondes

    def update(self, tilemap, movimiento=(0,0)): #agregamos tilemap para poder generaar la colision
        self.colision = {'up': False, 'down': False, 'right': False, 'left': False}       
        #choques en x
        mov_frame= (movimiento[0]+self.velocidad[0], movimiento[1]+self.velocidad[1])
        self.pos[0] +=mov_frame[0]
        rect_entidad= self.rect()#llamo al rect que maneja las colisiones, pasando posicion y tamaño en la funcion anterior
        #chequeo por colisiones de los rects del tile y de la entidad
        for rect in tilemap.mostrando_ubi_rects(self.pos):          
            if rect_entidad.colliderect(rect):  
                #asignamos un valor de x e y a traves del rect_entidad              
                if mov_frame[0]>0:                    
                    rect_entidad.right= rect.left #cuando choca y el frame es mayoor a cero, que el rect que va a la derecha, sea empujado hacia la izquierda
                    self.colision['right'] = True#acomoda la coordenada hacia la izquierda
                if mov_frame[0]<0:
                    rect_entidad.left= rect.right
                    self.colision['left'] = True
                self.pos[0]= rect_entidad.x #posicion en x      

        #choques en y
        self.pos[1] +=mov_frame[1]        
        rect_entidad= self.rect()        
        for rect in tilemap.mostrando_ubi_rects(self.pos):
            if rect_entidad.colliderect(rect):              
                if mov_frame[1]>0:
                    rect_entidad.bottom= rect.top #cuando choca y el frame es mayor a cero, que el rect que va a la derecha, sea empujado hacia la izquierda
                    self.colision['down'] = True
                if mov_frame[1]<0:
                    rect_entidad.top= rect.bottom
                    self.colision['up'] = True
                self.pos[1]= rect_entidad.y #posicion en y
                
        if movimiento[0]>0:
            self.rotar= False
        elif movimiento[0]<0:
            self.rotar= True

        self.velocidad[1]= min(5 , self.velocidad[1]+0.1)# gravedad
        
        if self.colision['down'] or self.colision['up']:
            self.velocidad[1] = 0

        self.animacion.update()      


    def dibujar(self, superficie, offset= (0,0)):
        imagen=pygame.transform.flip(self.animacion.img(),self.rotar,False)

        superficie.blit(imagen,(self.pos[0]-offset[0] + self.anim_offset[0], self.pos[1]- offset[1]+ self.anim_offset[1]))
       

class Golem(Entidadesfisicas):
    def __init__(self, juego,  pos, tamano):
        super().__init__(juego, 'golems', pos, tamano,)
        self.caminar=0
        self.ataque= False
        self.pos_golem=(0,0)
        self.ultimo_golpe = 0  # Almacena el tiempo del último disparo
        self.intervalo_golpe = 500

    def update(self, tilemap, movimiento=(0,0)):
        #logica del movimiento
        if self.ataque== False:            
            if self.caminar:#$obtenemos la ccoordenada del ccentro del rectangulo
                self.pos_golem=(self.rect().centerx + (-7 if self.rotar else 7), self.pos[1]+60)            
                if tilemap.chequear_choque(self.pos_golem):                
                    if (self.colision['right'] or self.colision['left']):                    
                        self.rotar = not self.rotar
                    else:
                        movimiento = (movimiento[0] - 0.5 if self.rotar else 0.5, movimiento[1])
                else:                
                    self.rotar = not self.rotar
                    
                self.caminar= max(0, self.caminar -1)
                
            elif (random.random()<0.01) :                            
                self.caminar = random.randint(30,120)   
        elif self.ataque:            
            movimiento= list(movimiento)
            movimiento[0]=0
            movimiento=tuple(movimiento)                   
        super().update(tilemap, movimiento)
        #configuramos ataque
        vision=pygame.Rect(self.pos_golem[0],self.pos_golem[1]-32, self.tamano[0]*(-1.1 if self.rotar else 1.1), self.tamano[1]) 
        if vision.colliderect(self.juego.jugador):
            self.ataque= True
            self.accion_actual('ataque')
            
            if (pygame.time.get_ticks() - self.ultimo_golpe > self.intervalo_golpe) and self.rect().colliderect(self.juego.jugador) :                
                self.juego.jugador.vida-=1
                self.juego.jugador.lastimar= True
                self.lastimar=True 
                self.ultimo_golpe=pygame.time.get_ticks()    
            else: 
                self.lastimar=False

        else:
            self.ataque=False
            if movimiento[0] != 0 :
                self.accion_actual('correr')            
            else:
                self.accion_actual('quieto')


class Arquero(Entidadesfisicas):
    def __init__(self, juego,pos, tamano, jugador): 
        super().__init__(juego, 'arquero', pos, tamano)       
        self.caminar=0            
        self.jugador= jugador
        self.tamano=tamano
        self.pos_arquero=(0,0)
        self.ataque= False
        self.ultimo_disparo = 0  # Almacena el tiempo del último disparo
        self.intervalo_disparo = 1500
    
    def update(self, tilemap, movimiento=(0,0)):
        if self.ataque== False:
            if self.caminar:#$obtenemos la ccoordenada del ccentro del rectangulo
                self.pos_arquero=(self.rect().centerx + (-10 if self.rotar else 10), self.pos[1]+60)
                
                if tilemap.chequear_choque(self.pos_arquero):                     
                    if (self.colision['right'] or self.colision['left']):                        
                        self.rotar = not self.rotar
                    else:
                        movimiento = (movimiento[0] - 0.5 if self.rotar else 0.5, movimiento[1])
                else:                   
                    self.rotar = not self.rotar                    
                self.caminar= max(1, self.caminar -2)
                
            elif (random.random()<0.01) :                            
                self.caminar = random.randint(30,120)
        elif self.ataque:           
            movimiento=list(movimiento)
            movimiento[0]=0
            movimiento=tuple(movimiento)

        vision=pygame.Rect(self.pos_arquero[0],self.pos_arquero[1]-60, 50*(-5 if self.rotar else 5), 10) 
        
        super().update(tilemap, movimiento)       

        if vision.colliderect(self.jugador):   
            self.ataque=True
            self.accion_actual('disparar')
            if pygame.time.get_ticks() - self.ultimo_disparo > self.intervalo_disparo:
                self.juego.flechas.append([[self.rect().centerx - 7, self.rect().centery], (-1.5 if self.rotar else 1.5), 0])                 
                self.ultimo_disparo=pygame.time.get_ticks()                 
        else:
            self.ataque=False
            if movimiento[0] != 0 :                
                self.accion_actual('correr')            
            else:                
                self.accion_actual('quieto') 

class Jugador(Entidadesfisicas):
    def __init__(self, juego,  pos, tamano, vida,respawn):        
        super().__init__(juego, 'jugador', pos, tamano)
        self.tiempo=0
        self.salto=3
        self.ataqueuno= False
        self.ataque=1
        self.vida=vida
        self.lastimar=False
        self.muerto= True
        self.score=0
        self.respawn=respawn         
    def update(self, tilemap, movimiento=(0,0)):
        super().update(tilemap, movimiento=movimiento)
        self.lastimar=False
        self.tiempo +=1
        if self.colision['down']:
            self.tiempo=0
            self.salto=3
        if self.tiempo==200:                       
            self.respawn-=1 
            self.muerto=True       
        
        if self.lastimar==True:
            self.accion_actual('lastimado')
        elif self.lastimar==False:
            if self.ataqueuno:  #cambiando el orden, hago que ataque saltando o no
                self.ataque_uno
                #ataque elimina genemigos
                for i in self.juego.golems.copy():
                    if self.rect().colliderect(i):
                        self.juego.golems.remove(i)
                        self.score+=100     
                for i in self.juego.arquero.copy():
                    if self.rect().colliderect(i):
                        self.juego.arquero.remove(i)
                        self.score+=500 
            elif self.tiempo>4:
                self.accion_actual('salto')            
            elif movimiento[0] != 0 :
                self.accion_actual('correr')            
            else:
                self.accion_actual('quieto')       

    def saltar(self):
        if self.salto>0:
            self.velocidad[1]=-4
            self.salto -=1
            self.tiempo =5

    def ataque_uno(self):         
        self.ataqueuno= True  
        self.accion_actual('ataque_uno')    
    
    def ataque_uno_false(self):
        self.ataqueuno= False

    def vidas(self, display, generador_fuente ):        
        imagen= pygame.image.load('data/imagenes/jugador/corazon/corazon.png')
        espacio=0
        for i in range(self.vida):             
            display.blit(imagen,(30 + espacio, 40 ))
            espacio+=50 
        texto= f'Puntaje: {self.score}'
        score = generador_fuente.render(texto, True, (0,0,0))            
        display.blit(score,(30,80))
    

  
              
        


