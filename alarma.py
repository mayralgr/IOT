# UNIR, Sensores, dispositivos, redes y protocolos de comunicacion
# Mayra Lucero Garcia Ramirez
# enviar una alarma si la temperatura y humedad alcanzan un valor umbral

# En el pin 7 existira un boton que activara o desactivara el control de temperatura. 
# En el pin 15 tendremos un led de alerta de temperatura. 
# En el pin 8 existira un boton que activara o desactivara el control de humedad
# En el pin 17 tendremos un led de alerta de humedad. 
# El led de alerta de temperatura se debera activar si la temperatura es mayor de 45 grados. 
# El led de alerta de humedad se debera activar si la humedad no esta entre el 25 y el 60 %. 
# El sistema debera realizar la comprobacion cada segundo. 

import RPi.GPIO as GPIO
import time
from sht21 import SHT21
# PINs
ledTemperatureAlertPin = 15
buttonTemperaturePin = 7
buttonHumidityPin = 8
ledHumidityAlertPin = 17
# Inicializacion de variables
temperatureAlert = False 
humidityAlert = False
prevTemperatureButtonState = True
buttonTemperatureState = True
prevHumidityButtonState = True
buttonHumidityState = True
currentTemperature = 0
currentHumidity = 0
print("Configurando modo Broadcom")
# Configuracion de Pines:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledTemperatureAlertPin, GPIO.OUT) 
GPIO.setup(ledHumidityAlertPin, GPIO.OUT) 
GPIO.setup(buttonTemperaturePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonHumidityPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Estado inicial de los botones e impresion de estado
buttonTemperatureState = GPIO.input(buttonTemperaturePin);
print "Estado inicial del boton de temperatura es ", 'presionado' if buttonTemperatureState else 'liberado';
buttonHumidityState = GPIO.input(buttonHumidityPin);
print "Estado inicial del boton de humedad es ", 'presionado' if buttonHumidityState else 'liberado';

# Estado inicial de leds = apagados
GPIO.output(ledTemperatureAlertPin, GPIO.LOW)
GPIO.output(ledHumidityAlertPin, GPIO.LOW)

# Estado inicial de temperatura y humedad
currentHumidity = SHT21(1).read_humidity()
currentTemperature = SHT21(1).read_temperature()
time.sleep(1) 
print("Empezando ejecucion, Presiona CTRL+C para salir")
try:
    while 1:
        # Obtener el estado de la activacion de alertas
        buttonTemperatureState = GPIO.input(buttonTemperaturePin);
        buttonHumidityState = GPIO.input(buttonHumidityPin);
        if prevTemperatureButtonState != buttonTemperatureState:
            print "El boton para la temperatura esta ", 'presionado' if buttonTemperatureState else 'liberado';
        if prevHumidityButtonState != buttonHumidityState:
            print "El boton para la humedad esta ", 'presionado' if buttonHumidityState else 'liberado';
        # guardar ultimo estado de los activadores de las alertas
        prevTemperatureButtonState = buttonTemperatureState;
        prevHumidityButtonState = buttonHumidityState;
        # obtener la temperatura y humedad
        currentHumidity = SHT21(1).read_humidity()
        currentTemperature = SHT21(1).read_temperature()
        # Impresion de control
        print "Temperatura: %s" % currentTemperature
        print "Humedad: %s" % currentHumidity
        # Configurar alertas
        temperatureAlert = currentTemperature > 45
        humidityAlert = currentHumidity < 25 or currentHumidity > 60
        # Validaciones
        if temperatureAlert and buttonTemperatureState:
            print ("Umbral alcanzado para la temperatura, El Led debe estar encendido");            
            GPIO.output(ledTemperatureAlertPin, GPIO.HIGH)
        if not temperatureAlert or not buttonTemperatureState:
            GPIO.output(ledTemperatureAlertPin, GPIO.LOW)
        if humidityAlert and buttonHumidityState:
            print ("Umbral alcanzado para la humedad, El Led de humedad debe estar encendido");            
            GPIO.output(ledHumidityAlertPin, GPIO.HIGH)
        if not humidityAlert or not buttonHumidityState:
            GPIO.output(ledHumidityAlertPin, GPIO.LOW)
        # Comprobacion cada segundo
        time.sleep(1)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO