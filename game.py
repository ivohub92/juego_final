import sys
import pygame
from constantes import *
from scripts.entidades import Entidadesfisicas, Jugador, Golem, Arquero
from scripts.utils import cargar_imagen, cargar_imagenes, Animacion, obtener_fuente
from scripts.tilemap import Tilemap
from scripts.nubes import Nubes
from data.menu.boton import Boton
from data.base_de_datos.base_datos import cargar_score, mostrar_score


class Juego:
    def __init__(self):

        pygame.init()
        
        pygame.display.set_caption('juego')
        
        self.display =pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.reloj= pygame.time.Clock()
        
        self.mov=[False, False]      
        self.assets= { #agrupo recursos graficos, etc
            'nubes': cargar_imagenes('nubes'),
            'grass': cargar_imagenes('tiles/grass'), #genero listas de imagenes de tiles
            'decor': cargar_imagenes('tiles/decor'),            
            'large_decor': cargar_imagenes('tiles/large_decor'),
            'stone': cargar_imagenes('tiles/stone'),
            'jugador': cargar_imagenes('jugador/quieto'),
            'golems': cargar_imagenes('golems/ataque'),    
            'arquero':cargar_imagenes('arquero/correr'),       
            'jugador/lastimado':  Animacion(cargar_imagenes('jugador/lastimado'),img_dur=6),
            'jugador/caminar':  Animacion(cargar_imagenes('jugador/caminar'),img_dur=4),
            'jugador/quieto': Animacion(cargar_imagenes('jugador/quieto'),img_dur=6),
            'jugador/correr': Animacion(cargar_imagenes('jugador/caminar'),img_dur=4),
            'jugador/salto': Animacion(cargar_imagenes('jugador/saltar'),img_dur=14),
            'jugador/ataque_uno': Animacion(cargar_imagenes('jugador/ataque_uno'),img_dur=4),
            'golems/ataque': Animacion(cargar_imagenes('golems/ataque'),img_dur=6),
            'golems/correr': Animacion(cargar_imagenes('golems/correr'),img_dur=6),
            'golems/quieto': Animacion(cargar_imagenes('golems/quieto'),img_dur=6),
            'arquero/disparar': Animacion(cargar_imagenes('arquero/disparar'),img_dur=6),
            'arquero/correr': Animacion(cargar_imagenes('arquero/correr'),img_dur=6),
            'arquero/quieto': Animacion(cargar_imagenes('arquero/quieto'),img_dur=6),
            'fondo': cargar_imagen('fondos/fondo_uno.jpg'),
            'flecha': cargar_imagen('flecha/flecha.png')
            
        }   

        #sonidos 
        self.sonido_pantalla= pygame.mixer.Sound('data/musica/pantalla.wav')
        self.sonido_salto= pygame.mixer.Sound('data/musica/salto.wav')
        self.sonido_golpe= pygame.mixer.Sound('data/musica/golpe.wav')
        self.sonido_golpe_jugador= pygame.mixer.Sound('data/musica/golpe_jugador.wav')
        self.sonido_ganador=pygame.mixer.Sound('data/musica/ganador.wav')
        self.sonido_nivel=pygame.mixer.Sound('data/musica/nivel.wav')  
        
        
        self.tilemap= Tilemap(self, tamano_tile=32)
        self.vida_jugador=VIDA_JUGADOR
        self.respawn_jugador=RESPAWN_JUGADOR
        self.jugador= Jugador(self,(50,50),(23,31),self.vida_jugador, self.respawn_jugador )#ultimo vectos. compenso que se hunde!!
        self.scroll=[0,0]       
        self.conteo=0
        self.dibujar_scroll=[0,0] 
        self.flechas=[]   
        self.nivel=1        
        self.ganador=False
        
    #CARGA LOS NIVELES Y TRAE LOS ENEMIGOS
    def cargar_nivel(self, map_id):
        self.sonido_nivel.play()
        self.tilemap.cargar('data/map'+str(map_id)+'.json')

        self.golems= []
        for golem in self.tilemap.extraer([('golems',0)]):                                                                                                                                                                                
            self.golems.append(Golem(self, golem['pos'],(23,32)))

        self.arquero= []        
        for arco in self.tilemap.extraer([('arquero',0)]):
            self.arquero.append(Arquero(self, arco['pos'],(23,32), self.jugador))

            
        for jugador in self.tilemap.extraer([('jugador',0)]):
            self.jugador.pos= jugador['pos']

    #MENU INICIAL
    def menu_inicio(self):
        pygame.mixer.init()
        self.sonido_pantalla.stop()        
        self.sonido_pantalla.play()
        self.jugador.vida= self.vida_jugador
        self.jugador.respawn= self.respawn_jugador
        while True:
            
            self.display.blit(pygame.image.load("data/menu/Background.png"), (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXTO = obtener_fuente(60).render("MENU PRINCIPAL", True, "#b68f40")
            MENU_RECT = MENU_TEXTO.get_rect(center=(ANCHO_VENTANA/2, 90))

            BOTON_JUGAR = Boton(imagen=pygame.image.load("data/menu/Play Rect.png"), escalar=0.8, pos=(ANCHO_VENTANA/2, 200), 
                                text_input="JUGAR", fuente=obtener_fuente(30), base_color="#d7fcd4")
            BOTON_OPCIONES = Boton(imagen=pygame.image.load("data/menu/Options Rect.png"), escalar=0.8,pos=(ANCHO_VENTANA/2, 320), 
                                text_input="PUNTAJES ALTOS", fuente=obtener_fuente(30), base_color="#d7fcd4")
            BOTON_SALIR = Boton(imagen=pygame.image.load("data/menu/Quit Rect.png"), escalar=0.8,pos=(ANCHO_VENTANA/2, 440), 
                                text_input="SALIR", fuente=obtener_fuente(30), base_color="#d7fcd4")

            self.display.blit(MENU_TEXTO, MENU_RECT)

            for botones in [BOTON_JUGAR, BOTON_OPCIONES, BOTON_SALIR]:                
                botones.update(self.display)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()               
                
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button==1:
                    if BOTON_JUGAR.checkClick(MENU_MOUSE_POS):
                        self.run()   
                    elif BOTON_OPCIONES.checkClick(MENU_MOUSE_POS):
                        self.ranking() 
                        
                    elif BOTON_SALIR.checkClick(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            
    #PANTALLA PUNTAJE FINAL
    def final_puntaje(self):        
        input_text = ""
        tecla_presionada= False
        advertencia=""

        while True:
            pygame.draw.rect(self.display, COLOR_BLANCO,(231,102,512,204))                      
            mostar_score = obtener_fuente(20).render(f'SCORE FINAL: {self.jugador.score}', True, (0,0,0)) 
            mostar_mensaje= obtener_fuente(20).render(f'INGRESE USUARIO:', True, (0,0,0))                      
            self.display.blit(mostar_score,(260,120)) 
            self.display.blit(mostar_mensaje,(260,150)) 
            if len(input_text)<3:
                advertencia=""
            else:
                advertencia= "MAX NOMBRE DE USUARIO: 3 CARACTERES"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()                
                elif event.type == pygame.KEYDOWN:            
                        
                        if event.key == pygame.K_RETURN: 
                            cargar_score(input_text, self.jugador.score, self.nivel)                     
                            self.menu_inicio()
                        elif event.key == pygame.K_BACKSPACE:                            
                            input_text = input_text[0:-1]
                        else:
                            if len(input_text)<3:
                                if not tecla_presionada:
                                    input_text += event.unicode                                
                                    tecla_presionada = True                                    
                            
                                    
                elif event.type == pygame.KEYUP:                    
                    tecla_presionada = False       
            texto= obtener_fuente(20).render(input_text, True, COLOR_NEGRO)
            self.display.blit(texto, (260,200))
            adv= obtener_fuente(10).render(advertencia, True, COLOR_NEGRO)
            self.display.blit(adv, (260,240))
            cartel= obtener_fuente(15).render('Presione enter para continuar', True, COLOR_NEGRO)
            self.display.blit(cartel, (260,280))

            if self.ganador:
                pygame.draw.rect(self.display, COLOR_BLANCO,(231,20,512,100))  
                cartel_ganador: cartel= obtener_fuente(20).render('GANASTE!!', True, COLOR_NEGRO)
                self.display.blit(cartel_ganador, (260,30))

                # Actualizar la pantalla            
            pygame.display.update()

    def ranking(self):       
            
        while True:
            self.display.blit(pygame.image.load("data/menu/Background.png"), (0, 0))
            pygame.draw.rect(self.display, COLOR_BLANCO,(ANCHO_VENTANA/8+100,ALTO_VENTANA/8,512,350)) 

            BOTON_OPCIONES = Boton(imagen=pygame.image.load("data/menu/Quit Rect.png"), escalar=0.4, pos=(ANCHO_VENTANA/2+100, 475), 
                                    text_input="ATRAS", fuente=obtener_fuente(20), base_color="#d7fcd4")
            BOTON_SALIR = Boton(imagen=pygame.image.load("data/menu/Quit Rect.png"), escalar=0.4, pos=(ANCHO_VENTANA/2-100,475), 
                                    text_input="SALIR", fuente=obtener_fuente(20), base_color="#d7fcd4")      
            for botones in [BOTON_OPCIONES, BOTON_SALIR]:                
                botones.update(self.display)     


            mostar_mensaje = obtener_fuente(20).render(f'PUNTAJES MAS ALTOS', True, (0,0,0))         
            self.display.blit(mostar_mensaje,(240,90)) 

            mostrar_score(self.display, obtener_fuente(15), 250, 150, 150,40)

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()               
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    print(MENU_MOUSE_POS )
                    if BOTON_OPCIONES.checkClick(MENU_MOUSE_POS):
                        print('click')
                        self.menu_inicio() 

                    if BOTON_SALIR.checkClick(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()       

                # Actualizar la pantalla            
            pygame.display.update()
    
    

    def run(self):
        self.sonido_pantalla.stop() 
        self.cargar_nivel(1)
        while True:
            self.display.blit(self.assets['fondo'],(0,0))            
            
            self.scroll[0] += (self.jugador.rect().centerx- self.display.get_width()/2- self.scroll[0])/30
            self.scroll[1] += (self.jugador.rect().centery- self.display.get_height()/2- self.scroll[1])/30
            self.dibujar_scroll = (int(self.scroll[0]), int(self.scroll[1]))     
              
         
            self.tilemap.dibujar(self.display,offset=self.dibujar_scroll)

            self.jugador.update(self.tilemap,(self.mov[1]-self.mov[0], 0))#updateo jugador, no el movimienot de la escena
            self.jugador.dibujar(self.display, offset=self.dibujar_scroll)
            
            if self.jugador.vida==0:                  
                self.jugador.respawn-=1 
                self.jugador.muerto=True
            elif self.jugador.vida<0:         
                self.jugador.muerto=True         
            if self.jugador.muerto== True:
                if self.jugador.respawn>0:                        
                    self.cargar_nivel(self.nivel)                    
                    self.jugador.muerto=False 
                    self.jugador.vida=self.vida_jugador                                  
                elif self.jugador.respawn==0:
                    self.final_puntaje()
        
        
            if len(self.golems.copy())==0 and len(self.arquero.copy())==0:                
                if self.nivel<3:
                    self.nivel +=1                    
                    self.cargar_nivel(self.nivel)                                        
                elif self.nivel==3 and len(self.golems.copy())==0 and len(self.arquero.copy())==0:                    
                    self.ganador=True
                    self.sonido_ganador.play()
                    self.final_puntaje()                    
                else:
                    self.ganador=False
                    self.final_puntaje()  
                    
                

            for golem in self.golems.copy():
                golem.update(self.tilemap, (0,0))
                golem.dibujar(self.display, self.dibujar_scroll)
                
            
            for arco in self.arquero.copy():
                arco.update(self.tilemap, (0,0))
                arco.dibujar(self.display, self.dibujar_scroll)
            
            for flecha in self.flechas.copy():                
                flecha[0][0] = flecha[1] + flecha[0][0]
                flecha[2] += 1
                img = self.assets['flecha']
                if flecha[1]>0:
                    rotar= False
                else:
                    rotar=True
                img=pygame.transform.flip(img,rotar,False)
                self.display.blit(img, (flecha[0][0] - img.get_width() / 2 - self.dibujar_scroll[0], flecha[0][1] - img.get_height() / 2 - self.dibujar_scroll[1]))
                if self.tilemap.chequear_choque(flecha[0]):
                    self.flechas.remove(flecha)                    
                elif flecha[2] > 360:
                    self.flechas.remove(flecha)
                elif self.jugador.rect().collidepoint(flecha[0]):
                    self.sonido_golpe.play()                                      
                    self.flechas.remove(flecha)
                    self.jugador.lastimar= True
                    self.jugador.vida -= 1 

            self.jugador.vidas(self.display, obtener_fuente(20))       

            lista_eventos= pygame.event.get()

            for evento in lista_eventos:
                if evento.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type==pygame.KEYDOWN:
                    if evento.key== pygame.K_LEFT:
                        self.mov[0]=True
                    if evento.key== pygame.K_RIGHT:
                        self.mov[1]=True
                    if evento.key == pygame.K_UP:
                        self.jugador.saltar()
                    if evento.key == pygame.K_z:
                        self.jugador.ataque_uno()
                        self.sonido_golpe_jugador.play()
                elif evento.type==pygame.KEYUP:
                    if evento.key== pygame.K_LEFT:
                        self.mov[0]=False
                    if evento.key== pygame.K_RIGHT:
                        self.mov[1]=False 
                    if evento.key == pygame.K_z:
                        self.jugador.ataque_uno_false()                  
            self.display.blit(self.display, (0, 0))
            pygame.display.update()
            self.reloj.tick(FPS)

Juego().menu_inicio()