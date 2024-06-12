# Autómatas celulares: juego de la vida de Conway
Los autómatas celulares datan de los años 1950, sin embargo su popularización empezo en 1970 cuando John Conway reveló al público el "Juego de la Vida". El autómata celular es un modelo matemático que consiste en un conjunto de celdas que cambian de estado de un momento a otro. Las propiedades que en un inicio son locales a un conjunto de celdas se pueden propagar por el sistema en general. **Berlekamp et al. (1982) demostró junto con el mismo Conway la universalidad del Juego de la Vida, que era posible construir una computadora con almacenamiento finito y es por tanto una Máquina de Turing**.

## Definición
Los autómatas celulares constan de los siguientes elementos:
* **Un espacio regular**: los autómatas celulares requieren de un espacio n-dimensional, por ejemplo el plano entero $Z\times Z$. El espacio puede ser finito o infinito.
* **Conjunto de estados**: un conjunto de estados finitos. Cada célula se encuentra en un estado del conjunto. En el juego de Conway se considera el conjunto $\{1,0\}$, interpretado en la célula como viva o muerta.
* **Estado inicial**: es la configuración inicial de los estados de las células en el espacio regular.
* **Vecindades**: se define como la vecindad de una célula como el conjunto de células que se pueden considerar adyacentes. En el juego de conway se consideran adyacentes a una célula (blanco) las 8 células de alrededor que forman un cuadrado (gris).

<div style="text-align:center;">
  <img src="https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcS505cLWb1nj7f33I31_gLVA9UEMbHyDDFNzP-emCdetqwqPCet" alt="square">
</div>

* **La función de transición del autómata**: es la misma para todas las células y depende de:
    * El estado actual de la célula.
    * El número de células vivas en su vecindad (entre 0 y 8).

    Se puede describir con la siguiente tabla:
  
|Estado actual\Estado de vecinos|0|1|2|3|4|5|6|7|8|
|-------------------------------|-|-|-|-|-|-|-|-|-|
|                0              |0|0|0|1|0|0|0|0|0|
|                1              |0|0|1|1|0|0|0|0|0|


# Implementación
Primero importamos los módulos necesarios:
* pygame: para crear la ventana principal y el bucle de juego.
* numpy: para generar la matriz vacía o plano principal de juego.
* time: para regular el tiempo entre las generaciones.

```Python
import pygame as pg
import numpy as np
import time
```

La implementación se puede entender de la siguiente manera:
* El espacio regular junto con los estados de cada célula se representa con una matriz de orden $50$, que inicialmente se encuentran sus valores en 0 (todas muertas).
* En un periodo $n$ se recorre cada célula $x$ -un elemento de la matriz-, y se obtiene la suma de los estados de sus vecinos. Según la cantidad de vecinos se asignará el estado de $x$ en el siguiente periodo $n+1$ según las reglas de transición. Para ello, el recorrido de cada célula se realiza en la matriz `estado`, y los cambios en el siguiente periodo se almacenan en la matriz `nuevo_estado`.
* El estado de cada célula se representa con un color: blanco para $1$ y gris oscuro para $0$. Un polígono blanco u oscuro es dibujado después de revisar su vecindad.
* La frontera en los bordes de la ventana se considera toroidal, esto es, los cambios en un extremo afectaran, si es necesario, al extremo opuesto.

En la implementación, además, se agregan detalles para experimentar con el autómata, como la posibilidad de modificar los estados directamente en el espacio y poner en "pausa" las transiciones al presionar alguna tecla.
```Python
# Constante
FONDO = (25, 25, 25)
# Inicio
pg.init()
# Pantalla
ancho = 600
alto = 600
# Celdas
nxC, nyC = 50, 50
dim_ancho = ancho / nxC
dim_alto = alto / nyC
# Estados
estado = np.zeros((nxC, nyC)) # Matriz
# Pausa
pausa = False
# Detalles de pantalla
pantalla = pg.display.set_mode((alto,ancho)) # Tamaño de ventana
pantalla.fill(FONDO) # Colorear ventana
pg.display.set_caption('Conway\'s Game') # Cambiar titulo

run = True
while run:
    # Copia
    nuevo_estado = np.copy(estado)
    # Superponer fondo
    pantalla.fill(FONDO)
    # Pausar ejecucion
    time.sleep(0.1)
    # Manejar eventos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            pausa = not pausa

        clic = [int(val) for val in pg.mouse.get_pressed()] # Convertir eventos True / False en 1 y 0
        if sum(clic) > 0: # Verificar si hay algun evento
            posX, posY = pg.mouse.get_pos()
            celX, celY = int(np.floor(posX / dim_ancho)), int(np.floor(posY / dim_alto)) # Obtener coordenadas de la celula
            nuevo_estado[celX, celY] = not clic[2] # Si no es el clic derecho, asignar 1
            
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pausa:
                # Vecinos
                vecinos = estado[(x - 1) % nxC, (y - 1) % nyC] + \
                          estado[(x) % nxC, (y - 1) % nyC]+\
                          estado[(x + 1) % nxC, (y - 1) % nyC] + \
                          estado[(x - 1) % nxC, (y) % nyC]+\
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

            # Coordenadas para dibujar un poligono cuadrado
            poly = [(x * dim_ancho, y * dim_alto), # Superior izquierdo
                    ((x+1) * dim_ancho, y * dim_alto), # Superior derecho
                    ((x+1) * dim_ancho, (y+1) * dim_alto), # Inferior derecho
                    (x * dim_ancho, (y+1) * dim_alto)] # Inferior izquierdo

            if nuevo_estado[x,y] == 0: 
                pg.draw.polygon(pantalla, (128,128,128), poly, 1) # Colorear celula viva
            else:
                pg.draw.polygon(pantalla, (255, 255, 255), poly, 0) # Colorear celula muerta
    # Actualizar juego
    estado = np.copy(nuevo_estado)
    # Actualizar
    pg.display.flip()
pg.quit()
```
