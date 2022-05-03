# UNIR, Sensores, dispositivos, redes y protocolos de comunicacion
# Mayra Lucero Garcia Ramirez
# enviar una alarma si la temperatura y humedad alcanzan un valor umbral

# En el pin 7 existira un boton que activara o desactivara el control de temperatura. 
# En el pin 15 tendremos un led de alerta de temperatura. 

import RPi.GPIO as GPIO
import time
alert = True 
ledAlertPin = 15

print("Setting Broadcom Mode")
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledAlertPin, GPIO.OUT) 

print("Here we go! Press CTRL+C to exit")
try:
    if alert:
            print ("Threshold met, LED SHOULD BE ON");            
            GPIO.output(ledAlertPin, GPIO.HIGH)

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO