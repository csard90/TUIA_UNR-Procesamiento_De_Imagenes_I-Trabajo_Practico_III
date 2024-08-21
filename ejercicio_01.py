import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import time # Esto solo lo usamos para control

# Funciones para eliminar lo que toque los bordes
def imreconstruct(marker, mask, kernel=None): 
    if kernel==None: # 
        kernel = np.ones((3,3), np.uint8)
    while True: 
        expanded = cv2.dilate(marker, kernel)                                       
        expanded_intersection = cv2.bitwise_and(src1=expanded, src2=mask)                       
        if (marker == expanded_intersection).all():                         
            break
        marker = expanded_intersection        
    return expanded_intersection

def imclearborder(img):
    marker = img.copy()               
    marker[1:-1,1:-1] = 0             
    border_elements = imreconstruct(marker=marker, mask=img)    
    img_cb = cv2.subtract(img, border_elements)                 
    return img_cb

# abs_path = 'D:\\Users\\csard 90\\Desktop\\TUIA\\Materias\\IV\\IA 4.4 Procesamiento de Imagenes I\\TP_03'
abs_path = 'E:\\UNR\\4 - Proc de Imágenes I (IA44)\\TP3\\PDI_TP3'
videos = ['tirada_1.mp4', 'tirada_2.mp4', 'tirada_3.mp4', 'tirada_4.mp4', 'tirada_5.mp4', 'tirada_6.mp4']
n=1

for video in videos:

    # Colocar la ruta absoluta
    cap = cv2.VideoCapture(os.path.join(abs_path, video))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Contador de frame en pantalla
    c = 0

    # Contador de frames donde los dados no se movieron
    contador_frames_quietos = 0

    out = cv2.VideoWriter(f'resolucion_tirada_{n}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width,height))
    n+=1
    while (cap.isOpened()):
        ret, frame = cap.read()

        # --- Control de frame actual ------------------------------------
        # print(f'Numero de frame: {c}')
        # ----------------------------------------------------------------

        if ret==True:        
            
            # ----------------------------------------------------------------
            # Identificar los margenes del paño
            
            # Segmentacion del paño con HSV
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            # plt.imshow(frame_rgb), plt.show()
            img_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV) 
            h, s, v = cv2.split(img_hsv)
            ix_h1 = np.logical_and(h > 65, h < 90)
            ix_s = np.logical_and(s > 75, s < 255)
            ix = np.logical_and(ix_h1, ix_s)

            b, g, r = cv2.split(frame)
            b[ix != True] = 0
            g[ix != True] = 0
            r[ix != True] = 0
            paño_img = cv2.merge((b, g, r))
            # plt.imshow(cv2.cvtColor(paño_img, cv2.COLOR_BGR2RGB), cmap='gray'), plt.show()
            
            # Pasamos la imagen del paño a escala de grises
            paño_gris = cv2.cvtColor(paño_img, cv2.COLOR_BGR2GRAY)
            # plt.imshow(frame_rgb, cmap='gray'), plt.show()

            # Umbralamos para obtener componentes conectadas, ponemos el valor minimo porque todo lo que 
            # quedo segmentado en HSV es paño.
            paño_umbralada = cv2.threshold(paño_gris, paño_gris.min(), 255, cv2.THRESH_BINARY)[1]
            # plt.imshow(paño_gris, cmap='gray'), plt.show()

            # Buscamos componentes conectadas para quedarnos solo con los pixels del bounding box del paño
            num_labels_paño, labels_paño, stats_paño, centroids_paño = cv2.connectedComponentsWithStats(paño_umbralada)  

            # Filtramos (el de mayor area es el paño)
            filtro_paño = np.argmax(stats_paño[:, -1])
            paño = stats_paño[filtro_paño]

            # Calculamos los limites del paño
            izquierda_paño = paño[cv2.CC_STAT_LEFT]
            derecha_paño = paño[cv2.CC_STAT_LEFT] + paño[cv2.CC_STAT_WIDTH]
            arriba_paño = paño[cv2.CC_STAT_TOP]
            abajo_paño = paño[cv2.CC_STAT_TOP] + paño[cv2.CC_STAT_HEIGHT]
            
            # Ya tenemos los valores de 'x' e 'y' para ubicar las coordenadas del paño

            # ---------------------------------------------------------------
            # # Paso 2 - Filtrar por color rojo los dados:

            # Filtramos por rojo
            ix_h1 = np.logical_and(h > 175, h < 180)
            ix_h2 = h < 10
            ix_s = np.logical_and(s > 150, s <= 255)            
            ix = np.logical_and(np.logical_or(ix_h1, ix_h2), ix_s)

            b, g, r = cv2.split(frame)
            b[ix != True] = 0
            g[ix != True] = 0
            r[ix != True] = 0
            dados = cv2.merge((b, g, r))
            # plt.imshow(cv2.cvtColor(dados, cv2.COLOR_BGR2RGB)), plt.show()

            # Pasamos la imagen del paño a escala de grises
            dados_gris = cv2.cvtColor(dados, cv2.COLOR_BGR2GRAY)
            # plt.imshow(dados_gris, cmap='gray'), plt.show()

            # Umbralamos para obtener componentes conectadas, nuevamente como filtramos por color rojo
            # queremos que nos quede todo lo fitrado (los dados) por eso el umbral es del minimo valor
            # de gris en adelante
            dados_umbralada = cv2.threshold(dados_gris, dados_gris.min(), 255, cv2.THRESH_BINARY)[1]
            # plt.imshow(dados_umbralada, cmap='gray'), plt.show()

            # Buscamos componentes conectadas para despues quedarnos con los dados
            num_labels_dados, labels_dados, stats_dados, centroids_dados = cv2.connectedComponentsWithStats(dados_umbralada)              
            
            indice_dados_sobre_paño = []

            # Verificamos que los elementos tengan determinada area, esten sobre el bounding box del paño y la 
            # relacion de aspecto, esto es porque la imagen queda con elementos mas pequeños que los dados y 
            # mas grande (fondo)
            for j in range(1, len(stats_dados)):
                
                # Si cumplen con el intervalo de area aceptable
                if (stats_dados[j, -1] > 2300) & (stats_dados[j, -1] < 4450):

                    # Calculamos los valores en 'x' e 'y' donde estan los dados
                    izquierda_dado = stats_dados[j, cv2.CC_STAT_LEFT]
                    derecha_dado = stats_dados[j, cv2.CC_STAT_LEFT] + stats_dados[j, cv2.CC_STAT_WIDTH]
                    arriba_dado = stats_dados[j, cv2.CC_STAT_TOP]
                    abajo_dado = stats_dados[j, cv2.CC_STAT_TOP] + stats_dados[j, cv2.CC_STAT_HEIGHT]

                    # Calculamos el ancho y alto para relacion de aspecto
                    ancho_dado = derecha_dado-izquierda_dado
                    alto_dado = abajo_dado-arriba_dado

                    # Chequeamos que efectivamente este sobre el paño, si esta sobre el paño:
                    if (izquierda_dado  >= izquierda_paño and izquierda_dado  <= derecha_paño) and \
                        (derecha_dado >= izquierda_paño and derecha_dado <= derecha_paño) and \
                        (arriba_dado >= arriba_paño and arriba_dado <= abajo_paño) and \
                        (abajo_dado >= arriba_paño and abajo_dado <= abajo_paño):
                        
                        # Y ademas chequeamos que tenga cierta relacion de aspecto
                        if (alto_dado/ancho_dado > 0) and (alto_dado/ancho_dado < 10):

                            # Añadimos a la lista que de indices de elementos con los que nos vamos a quedar:
                            indice_dados_sobre_paño.append(j)          
     
            # Esto cobra sentido a partir del segundo frame (de c=1 en adelante)
            if c != 0: 
                dados_anterior = dados_actual
                centroides_anterior = centroides_actual   

            # Filtramos los stats con los elementos que nos quedamos
            dados_actual = stats_dados[indice_dados_sobre_paño]

            # Y tambien filtramos los centroides con los elementos que nos quedamos
            centroides_actual = centroids_dados[indice_dados_sobre_paño]

            
            # Hasta ahora ya tenemos detectado el paño (para verificar que los dados esten sobre el mismo) y
            # tenemos segmentados y filtrados luego los elementos del color de los dados con determinada area
            # y relacion de aspecto.
                        

            # ------------------------------- Control --------------------------------------
            # print(f'Dados detectados:\n{dados_actual}')
            # print(f'Centroides detectados:\n{centroides_actual}')
            # ------------------------------------------------------------------------------

            # Mostrar el nombre del video en el frame
            cv2.putText(frame, "Video Analizado:", (75, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"[ {video} ]", (150, 220), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            
            resultado_final = frame.copy() 

            # Si:
            # 1. no estamos en el primer frame, porque en el primer frame no van a existir las estadisticas
            # de los datos anteriores para comparar, 
            # 2. en la anterior iteracion se detectaron la misma cantidad de datos que ahora, porque
            # no podemos calcular la distancia euclidea en dos matrices con diferente longitud
            # 3. si se detectaron los 5 dados porque necesitamos una cantidad fija constante de dados
            # ya que trabajamos con las distancias de los centroides del anterior frame y el actual,
            # si en una iteracion tenemos mas dados y en la proxima menos no podremos calcular si estos
            # se movieron con este algoritmo

            # Esto tiene sentido a partir de la segunda iteracion (c=1)
            if (c!= 0) and (len(dados_actual) == len(dados_anterior)) and (len(dados_actual)==5):

                # Entonces calculamos la distancia euclidea
                diferencia = centroides_anterior - centroides_actual
                distancia = np.sqrt(np.sum(diferencia**2, axis=1)).reshape(-1,1)
                
                # Si esta distancia es menor a determinado umbral en todo el array significa que los dados 
                # estuvieron quietos
                if all(distancia < 5):
                    # Entonces llevamos un frame con los dados en ese estado (quietos)
                    contador_frames_quietos+=1
                # Caso contrario re-incializamos el contador para empezar de 0 la proxima
                # que se cumplan las condiciones
                else: 
                    contador_frames_quietos=0
                    numeros_dados = []
                
                # -------------------------------Control----------------------------------------
                # print(f'Diferencia centroides:\n{distancia}')
                # ------------------------------------------------------------------------------
                
                # Si los dados estuvieron quietos mas de determinada cantidad de frames
                if contador_frames_quietos > 5:

                    # Recorremos las estadisticas de los dados detectados
                    for i in range(len(dados_actual)):
                        # Dibujamos el rectangulo en cada uno
                        resultado_final = cv2.rectangle(resultado_final, \
                                            (dados_actual[i, cv2.CC_STAT_LEFT], dados_actual[i, cv2.CC_STAT_TOP]), 
                                            (dados_actual[i, cv2.CC_STAT_LEFT]+dados_actual[i, cv2.CC_STAT_WIDTH] , 
                                            dados_actual[i, cv2.CC_STAT_TOP]+dados_actual[i, cv2.CC_STAT_HEIGHT]), \
                                            (255, 0, 0), 4)

                        # -------------------------- Contar nro dados ---------------------------------                        
                        # El numero de los dados lo contamos una unica vez, porque si lo intentamos contar en cada frame muchas
                        # veces de un frame a otro las imagenes son distintas, son muchos frames por video, sumado a que cuando
                        # la mano pasa por encima ocurre que cambia el nivel de gris cuando lo intentamos hacer dinamico 
                        # ha pasado que en dos frames de dos videos nos dio mal el numero del dado. De este modo va a dar siempre
                        # bien, y tambien tiene sentido porque los dados estan detenidos, el numero no va a cambiar.
                        if contador_frames_quietos == 6:
                            
                            # Nos quedamos con el boundig-box del dado en cuestion
                            recorte_dado = frame[dados_actual[i, cv2.CC_STAT_TOP]: \
                                                 dados_actual[i, cv2.CC_STAT_TOP]+dados_actual[i, cv2.CC_STAT_HEIGHT], \
                                                 dados_actual[i, cv2.CC_STAT_LEFT]:dados_actual[i, \
                                                 cv2.CC_STAT_LEFT]+dados_actual[i, cv2.CC_STAT_WIDTH]]
                            # plt.imshow(recorte_dado), plt.show()
                            # Pasamos a RGB
                            recorte_dado_rgb = cv2.cvtColor(recorte_dado, cv2.COLOR_BGR2RGB) 
                            # plt.imshow(recorte_dado_rgb), plt.show()
                            # Pasamos a escala de grises
                            recorte_dado_gris = cv2.cvtColor(recorte_dado_rgb, cv2.COLOR_BGR2GRAY)
                            # plt.imshow(recorte_dado_gris, cmap='gray'), plt.show()
                            
                            # Umbralamos para quedarnos con los circulos
                            recorte_dado_umbralada = cv2.threshold(recorte_dado_gris, 85, 255, cv2.THRESH_BINARY)[1]
                            # plt.imshow(recorte_dado_umbralada, cmap='gray'), plt.show()

                            # Eliminamos todo lo que toque los bordes
                            recorte_dado_bordes = imclearborder(recorte_dado_umbralada)
                            # plt.imshow(recorte_dado_bordes, cmap='gray'), plt.show()

                            # Componentes conectadas
                            num_labels_recorte_dado, labels_recorte_dado, stats_recorte_dado, \
                                centroids_recorte_dado = cv2.connectedComponentsWithStats(recorte_dado_bordes)  
                            # print(stats_recorte_dado)

                            # Filtro por area
                            filtro_recorte_dado = (stats_recorte_dado[:, -1] > 55) & (stats_recorte_dado[:, -1] < 180)

                            # Calculamos el numero con la longitud del array filtrado con los stats
                            numero_dado = len(stats_recorte_dado[filtro_recorte_dado])
                            
                            # Guardamos los numeros por unica vez en la lista
                            numeros_dados.append(numero_dado)

                        # A partir de ahora en cada iteracion escribimos el numero correspondiente al dado
                        # i que esta guardada en la posicion i de la lista anterior
                        resultado_final = cv2.putText(resultado_final, f'{str(numeros_dados[i])}', \
                                (dados_actual[i, cv2.CC_STAT_LEFT]+15,dados_actual[i, cv2.CC_STAT_TOP]-15), \
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                        # plt.imshow(cv2.cvtColor(resultado_final, cv2.COLOR_BGR2RGB)), plt.show()                                            
    
            # Mostramos por pantalla
            frame_show = cv2.resize(resultado_final, dsize=(int(width/3), int(height/3)))
            cv2.imshow('Frame', frame_show)
            
            # Grabar video:
            out.write(resultado_final)  # grabo frame --> IMPORTANTE: frame debe tener el mismo tamaño que se definio al crear out.

            # Suma 1 contador de frames
            c+=1

            # --------------------------- Control ------------------------------
            # if c >=88: time.sleep(2) # Para que los frames vayan mas lentos
            # ------------------------------------------------------------------

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

