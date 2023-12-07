import sqlite3
import pygame
def cargar_score(usuario, score,nivel):
    with sqlite3.connect("datos_score.db") as conexion:
        try:
            sentencia = ''' create  table ranking
            (
            id integer primary key autoincrement,
            Usuario text,
            Score text,
            Nivel text
            )
            '''
            conexion.execute(sentencia)
            print("Se creo la tabla ")                       
        except sqlite3.OperationalError:
            print("La tabla ya existe")

        #INSERT:       
        sql_insertar= "INSERT INTO ranking (usuario, score, nivel) VALUES (?,?,?)"
        usuario= usuario
        score=score
        nivel= nivel
        try:
            conexion.cursor().execute(sql_insertar, (usuario, score, nivel ))           
        except:
            print("Error")

def mostrar_score(display, fuente, posicion_x, posicion_y, espaciado_x, espaciado_y):    
    usuario_render= fuente.render('USUARIO', True, (0,0,0))
    display.blit(usuario_render, (250, 130))
    puntaje_render= fuente.render('PUNTAJE', True, (0,0,0))
    display.blit(puntaje_render, (400, 130))
    nivel_render= fuente.render('NIVEL', True, (0,0,0))
    display.blit(nivel_render, (550, 130))
        
    with sqlite3.connect("datos_score.db") as conexion:
        try:
            cursor = conexion.cursor()#Un objeto de cursor actúa como un puntero o indicador de posición dentro 
            #de un conjunto de resultados devueltos por una consulta SQL.
            # Seleccionar los primeros 5 registros ordenados por score de mayor a menor
            cursor.execute("SELECT * FROM ranking ORDER BY Score DESC LIMIT 5")
            filas = cursor.fetchall() #recupero todas las filas con el cursor de python

            # Mostrar los datos en la pantalla       
            
            y = posicion_y       
            x =posicion_x
            x_dos= posicion_x + espaciado_x
            x_tres= posicion_x + espaciado_x*2          

            for fila in filas:         
            
                usuarios= f"{fila[1]}" 
                usuarios_render = fuente.render(usuarios, True, (0,0,0))
                display.blit(usuarios_render, (x, y))
                score= f"{fila[2]}" 
                score_render = fuente.render(score, True, (0,0,0))
                display.blit(score_render, (x_dos, y))
                nivel= f"{fila[3]}"
                nivel_render = fuente.render(nivel, True, (0,0,0))
                display.blit(nivel_render, (x_tres, y))
                
                y += espaciado_y 
        except sqlite3.OperationalError:
            print("Error")