import pygame as pg
import numpy as np
import time
# Constante
fondo = (25, 25, 25)
# Inicio
pg.init()

# Pantalla
ancho = 600
alto = 600
pantalla = pg.display.set_mode((alto,ancho))
pantalla.fill(fondo)
pg.display.set_caption('Conway\'s Game')
# Celdas
nxC, nyC = 50, 50
dim_ancho = ancho / nxC
dim_alto = alto / nyC
# Estados
estado = np.zeros((nxC, nyC))

# Pausa
pausa = False
# Bucle de juego
run = True
while run:

    # Copia
    nuevo_estado = np.copy(estado)

    pantalla.fill(fondo)

    time.sleep(0.1)
    # Handle event
    for event in pg.event.get():
        # if event.type == pg.KEYDOWN:
        # pausa = not pausa
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            pausa = not pausa

        clic = [int(val) for val in pg.mouse.get_pressed()]
        if sum(clic) > 0:
            posX, posY = pg.mouse.get_pos()
            celX, celY = int(np.floor(posX / dim_ancho)), int(np.floor(posY / dim_alto))
            nuevo_estado[celX, celY] = not clic[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pausa:
            # Vecinos
                vecinos = estado[(x - 1) % nxC, (y - 1) % nyC] + \
                          estado[(x) % nxC, (y - 1) % nyC]+\
                          estado[(x + 1) % nxC, (y - 1) % nyC] + \
                          estado[(x - 1) % nxC, (y) % nyC] + \
                          estado[(x + 1) % nxC, (y) % nyC] + \
                          estado[(x - 1) % nxC, (y + 1) % nyC] + \
                          estado[(x) % nxC, (y + 1) % nyC] + \
                          estado[(x + 1) % nxC, (y + 1) % nyC]
                # Regla 1: Celula con 3 vecinas revive
                if estado[x,y] == 0 and vecinos == 3:
                    nuevo_estado[x,y] = 1
                # Regla 2: Celula viva con menos de 2 o mas de 3 vecinas, muere
                elif estado[x,y] == 1 and (vecinos < 2 or vecinos > 3):
                    nuevo_estado[x,y] = 0

            poly = [(x * dim_ancho, y * dim_alto),
                    ((x+1) * dim_ancho, y * dim_alto),
                    ((x+1) * dim_ancho, (y+1) * dim_alto),
                    (x * dim_ancho, (y+1) * dim_alto)]

            if nuevo_estado[x,y] == 0:
                pg.draw.polygon(pantalla, (128,128,128), poly, 1)
            else:
                pg.draw.polygon(pantalla, (255, 255, 255), poly, 0)

    # Actualizar juego
    estado = np.copy(nuevo_estado)

    # Actualizar
    pg.display.flip()

pg.quit()