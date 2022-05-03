# UNIR, Sensores, dispositivos, redes y protocolos de comunicacion
# Mayra Lucero Garcia Ramirez
# enviar una alarma si la temperatura y humedad alcanzan un valor umbral

# En el pin 7 existira un boton que activara o desactivara el control de temperatura. 
# En el pin 15 tendremos un led de alerta de temperatura. 

import RPi.GPIO as GPIO
import time
# PINs
ledAlertPin = 15
buttonTemperaturePin = 7
buttonHumidityPin = 8

# Initial variables
alert = True 
prevTemperatureButtonState = True
buttonTemperatureState = True
prevHumidityButtonState = True
buttonHumidityState = True

print("Setting Broadcom Mode")
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledAlertPin, GPIO.OUT) 
GPIO.setup(buttonTemperaturePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonHumidityPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Initial button state
#print initial settings
buttonTemperatureState = GPIO.input(buttonTemperaturePin);
print "Initial temperature state is ", 'pressed' if buttonTemperatureState else 'released';
buttonHumidityState = GPIO.input(buttonHumidityPin);
print "Initial temperature state is ", 'pressed' if buttonHumidityState else 'released';

# Initial led state
GPIO.output(ledAlertPin, GPIO.LOW)


print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        buttonTemperatureState = GPIO.input(buttonTemperaturePin);
        buttonHumidityState = GPIO.input(buttonHumidityPin);
        if prevTemperatureButtonState != buttonTemperatureState:
            print "Button for temperature is ", 'pressed' if buttonTemperatureState else 'released';
        if prevHumidityButtonState != buttonHumidityState:
            print "Button for humidity is ", 'pressed' if buttonHumidityState else 'released';
        # save last state
        prevTemperatureButtonState = buttonTemperatureState;
        prevHumidityButtonState = buttonHumidityState;    
        time.sleep(0.1) 
        if alert:
                print ("Threshold met, LED SHOULD BE ON");            
                GPIO.output(ledAlertPin, GPIO.HIGH)

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO