import sys
import pygame
from constantes import *
from scripts.utils import cargar_imagenes
from scripts.tilemap import Tilemap



class Editor:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('editor')
        self.display= pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))        
        self.reloj= pygame.time.Clock()
        
             
        self.assets= { #agrupo recursos graficos,
            'nubes': cargar_imagenes('nubes'),
            'grass': cargar_imagenes('tiles/grass'), #genero listas de imagenes de tiles
            'decor': cargar_imagenes('tiles/decor'),            
            'large_decor': cargar_imagenes('tiles/large_decor'),            
            'stone': cargar_imagenes('tiles/stone'),  
            'golems': cargar_imagenes('golems/ataque'),
            'arquero':cargar_imagenes('arquero/correr'),   
            'jugador': cargar_imagenes('jugador/quieto'),
            'corazon': cargar_imagenes('jugador/corazon')
        }       
        self.mov=[False, False, False, False]

        #cargo tilemaps
        self.tilemap= Tilemap(self, tamano_tile=32)  
        try:
            self.tilemap.cargar('map.json')
        except FileNotFoundError:
            pass #trata de cagraG EL JSON del nivel si ya existe. Sino lo pasa de largo

        self.scroll=[0,0]#Paso como lista primero
        self.lista_tilemap= list(self.assets)
        self.tile_grupo=0 
        self.tile_tipo=0 
        #variables usadas para manejar la edicion de los tiles
        self.click= False
        self.click_derecho= False
        self.shift= False
        self.on_grid= True
        

    def run(self):
        while True:
            self.display.fill((0,0,0))

            self.scroll[0]+= (self.mov[1]-self.mov[0])*2 
            self.scroll[1]+= (self.mov[3]-self.mov[2])*2
            
            render_scroll= (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tilemap.dibujar(self.display, render_scroll) #dibuja lo de las listas

            img_tile_actual= self.assets[self.lista_tilemap[self.tile_grupo]][self.tile_tipo].copy()
            img_tile_actual.set_alpha(100)
            map_pos= pygame.mouse.get_pos() 

            tile_pos= (int((self.scroll[0]+map_pos[0])//self.tilemap.tamano_tile), int((self.scroll[1]+map_pos[1])//self.tilemap.tamano_tile)  )#devuelve valor de coordenada en funcion de mi sistema de tiles

            if self.on_grid:
                self.display.blit(img_tile_actual, (tile_pos[0]*self.tilemap.tamano_tile-self.scroll[0],tile_pos[1]*self.tilemap.tamano_tile-self.scroll[1]))#muestra lo que estoy llevando. Es para diseñar mas simple
            else:
                self.display.blit(img_tile_actual, map_pos)

            if self.click and self.on_grid:
                self.tilemap.tilemap[str(tile_pos[0])+';'+ str(tile_pos[1])]={'categoria':self.lista_tilemap[self.tile_grupo],'tipo': self.tile_tipo, 'pos': tile_pos  }
            
            if self.click_derecho:
                tile_ubi= (str(tile_pos[0]) + ';'+ str(tile_pos[1]))
                if tile_ubi in self.tilemap.tilemap:#si existe, que lo borre
                    del self.tilemap.tilemap[tile_ubi]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img= self.assets[tile['categoria']][tile['tipo']]
                    tile_rect= pygame.Rect(tile['pos'][0]-self.scroll[0], tile['pos'][1]-self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_rect.collidepoint(map_pos):
                        self.tilemap.offgrid_tiles.remove(tile)
            


            self.display.blit(img_tile_actual,(10,10))            
            
            lista_eventos= pygame.event.get()

            for evento in lista_eventos:
                if evento.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type== pygame.MOUSEBUTTONDOWN:
                    if evento.button==1:
                        self.click= True
                        if not self.on_grid:
                            self.tilemap.offgrid_tiles.append({'categoria': self.lista_tilemap[self.tile_grupo], 'tipo': self.tile_tipo, 'pos': (self.scroll[0]+map_pos[0],self.scroll[1]+map_pos[1])})
                    if evento.button==3:
                        self.click_derecho= True
                    if self.shift:#vemos las variantes de tile/pj
                        if evento.button==4:#rueda scroll arribas
                            self.tile_tipo= (self.tile_tipo-1) % len(self.assets[self.lista_tilemap[self.tile_grupo]])      # Calcula el módulo del resultado anterior con la longitud de grupos.
                            #Esto se hace para asegurarse de que self.tile_tipo esté en el rango válido de índices para la lista de activos.                        
                        if evento.button==5:#rueda scroll abajo
                            self.tile_tipo= (self.tile_tipo+1) % len(self.assets[self.lista_tilemap[self.tile_grupo]]) 
                        
                    else:#rueda cambia tipo de tile/personaje
                        if evento.button==4:#rueda scroll arribas
                            self.tile_grupo= (self.tile_grupo-1) % len(self.lista_tilemap)  
                            self.tile_tipo=0 #corrijo posible error de index                          
                        if evento.button==5:#rueda scroll abajo
                            self.tile_grupo= (self.tile_grupo+1) % len(self.lista_tilemap)
                            self.tile_tipo=0 #corrijo posible error de index

                if evento.type== pygame.MOUSEBUTTONUP:
                    if evento.button==1:
                        self.click= False
                        
                    if evento.button==3:
                        self.click_derecho= False                        
                            

                if evento.type==pygame.KEYDOWN:
                    if evento.key== pygame.K_LEFT:
                        self.mov[0]=True
                    if evento.key== pygame.K_RIGHT:
                        self.mov[1]=True
                    if evento.key == pygame.K_UP:
                        self.mov[2]=True
                    if evento.key == pygame.K_DOWN:
                        self.mov[3]=True
                    if evento.key== pygame.K_LSHIFT:
                        self.shift= True
                    if evento.key== pygame.K_g:
                        self.on_grid= not self.on_grid
                    if evento.key== pygame.K_o:
                        self.tilemap.guardar('map.json')
                elif evento.type==pygame.KEYUP:
                    if evento.key== pygame.K_LEFT:
                        self.mov[0]=False
                    if evento.key== pygame.K_RIGHT:
                        self.mov[1]=False
                    if evento.key == pygame.K_UP:
                        self.mov[2]=False
                    if evento.key == pygame.K_DOWN:
                        self.mov[3]=False
                    if evento.key== pygame.K_LSHIFT:
                        self.shift= False
                   
                    
            self.display.blit(self.display, (0, 0))
            pygame.display.flip()
            self.reloj.tick(FPS)

Editor().run()