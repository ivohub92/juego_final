import json
import pygame

#CATEGORIA == TYPE

MOSTRANDO_TILES=  [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]#uso para iterar y evitar errores de redondeo en grilla
SUELO_TILES={ 'grass' , 'stone' }
class Tilemap:
    def __init__(self, juego, tamano_tile=33):
        self.juego= juego
        self.tamano_tile=tamano_tile
        self.tilemap={}#la ventaja de declarar los tiles de esta manera, es que si lo hacemos por listas hay que llenar los espacios en 
        #blanco con ceros. En cambio usar diccionarios es mas facil ya que no precisa que haga este llenado ya que puedo asignar directamente
        #por coordenadas (x,y)
        self.offgrid_tiles=[]
        #generamos cada tile usando las posiciones dinamicas y asignando un tipo a cada tile
           #en x
            #en y. Las posiciones deben coincidir
            #le asigmo posiciones al tile
            #dinamicamente, donde tengo una coreccion de 3 entonces va de 3 a 12 en x e y mantenemos constante
    #renderizar tiles
    #cada tile posee una categoria y una variable para usarla despues
    #la categoria se busca en assets y el tipo de suelo coincide con la posicion en la lista genera en 
    #la funcion cargar_imagenes
    

    def mostrando_ubi_tiles(self, pos):#usamos pixeles!-> Convertimos la posicion de pixel en posicion (x,y). Armamos una lista
        tiles=[]                        #con la info de los tiles que va pasando el personaje 
        tile_ubicacion=(int(pos[0] // self.tamano_tile),int(pos[1] // self.tamano_tile))# si bien // elimina el resto en su operacion, puede caber la posibilidad
        for offset in MOSTRANDO_TILES:#de que se escape un .00 asi que usamos int para eliminar cualquier posibilidad. No hacemos directo el int porque este trunca el numero
            check_ubicacion= str(tile_ubicacion[0] + offset[0])+ ';' + str(tile_ubicacion[1] + offset[1])#no toma en consideracion la operacion, cosa que el // si hace. Esta diferencia se ve con los numeros negativos
            if check_ubicacion in self.tilemap:    #Verificamos qu efectivamente alla un tile en la lista que traemos del json
                tiles.append(self.tilemap[check_ubicacion])
        return tiles
    
    #extraer tipos de tiles especificos (uso para enemigos en este caso)
    def extraer(self, id_pares, keep=False):
        match = []
        for tile in self.offgrid_tiles.copy(): #buscar pares coincidentes en los tiles y generar enemmigos
            if (tile['categoria'], tile['tipo']) in id_pares:
                match.append(tile.copy())#copiamos poirque probablkemente querramos borrar de la lista asi no modificamos el original
                if not keep:
                    self.offgrid_tiles.remove(tile)        
        return match


    def guardar(self, path):
        f= open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tamano_tile': self.tamano_tile, 'offgrid': self.offgrid_tiles},f)
        f.close()
    
    def cargar(self, path):
        
        f= open(path, 'r')
        map_data= json.load(f)
        f.close()
        self.tilemap= map_data['tilemap']
        self.tamano_tile= map_data['tamano_tile']
        self.offgrid_tiles= map_data['offgrid']

    def chequear_choque(self, pos): #verificvamos si existe y si es asi, que nos devuelva.        
        tile_ubi = str(int(pos[0] // self.tamano_tile)) + ';' + str(int(pos[1] // self.tamano_tile)) #por alguna razon qyue no entiend (matematica, supongo), no checkea bien pero si lo hace agregando +1 como factor de correcion       
    
        if tile_ubi in self.tilemap:                      
            if self.tilemap[tile_ubi]['categoria'] in SUELO_TILES:#chequeamos que sea tile
                return self.tilemap[tile_ubi]      #funciona como true en este caso
        
    def mostrando_ubi_rects(self, pos):#genero una lista de rects a usar
        rects=[]
        for tile in self.mostrando_ubi_tiles(pos):            
            if tile['categoria'] in SUELO_TILES:                
                rects.append(pygame.Rect(tile['pos'][0]*self.tamano_tile,tile['pos'][1]*self.tamano_tile, self.tamano_tile, self.tamano_tile))
        return rects

    def dibujar(self, superficie,  offset=(0,0)):
        for tile in self.offgrid_tiles: 
            superficie.blit(self.juego.assets[tile['categoria']][tile['tipo']], (tile['pos'][0]- offset[0], tile['pos'][1]-offset[1]) ) #las posiciones se restan porque si me muevo a la derecha, todo se corre a la izquierda 

        for x in range(offset[0] // self.tamano_tile, (offset[0]+ superficie.get_width()) // self.tamano_tile +1 ):#+1 porque corrige el error de offset 
            for y in range(offset[1] // self.tamano_tile, (offset[1]+ superficie.get_height()) // self.tamano_tile +1 ):
                ubicacion= str(x) + ';'+ str(y)
                if ubicacion in self.tilemap:
                    tile= self.tilemap[ubicacion]## determino con este calculo que tiles se muestran en pantalla asi renderizo solo esto
                    superficie.blit(self.juego.assets[tile['categoria']][tile['tipo']], (tile['pos'][0] *self.tamano_tile -offset[0] , tile['pos'][1]*self.tamano_tile-offset[1]))
            #con la altura pasa igual, ya que son coordenadas.
            #agrego offset, que hace que se mueva todo el escenario, dando la ilusion que se mueve el personaje(se mueven ambos pero    
            # en sentidos opuestos para estabilizar la camara)
            #offgrid se usa para elementos por fuera de la grilla. OJO! No confundir porque sino da errores