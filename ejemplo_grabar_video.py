import cv2

# --- Leer y grabar un video ------------------------------------------------
cap = cv2.VideoCapture('tirada_1.mp4')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

out = cv2.VideoWriter('Video-Output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width,height))
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # --- Procesamiento ---------------------------------------------
        cv2.rectangle(frame, (100,100), (200,200), (0,0,255), 2)

        # --- Muestro por pantalla ------------
        frame_show = cv2.resize(frame, dsize=(int(width/3), int(height/3)))
        cv2.imshow('Frame',frame_show)
        # ---------------------------------------------------------------
        out.write(frame)  # grabo frame --> IMPORTANTE: frame debe tener el mismo tamaño que se definio al crear out.
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
