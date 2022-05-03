# UNIR, Sensores, dispositivos, redes y protocolos de comunicacion
# Mayra Lucero Garcia Ramirez
# enviar una alarma si la temperatura y humedad alcanzan un valor umbral

# En el pin 7 existira un boton que activara o desactivara el control de temperatura. 
# En el pin 15 tendremos un led de alerta de temperatura. 

import RPi.GPIO as GPIO
import time
from sht21 import SHT21
# PINs
ledTemperatureAlertPin = 15
buttonTemperaturePin = 7
buttonHumidityPin = 8
ledHumidityAlertPin = 17
# Initial variables
temperatureAlert = False 
humidityAlert = False
prevTemperatureButtonState = True
buttonTemperatureState = True
prevHumidityButtonState = True
buttonHumidityState = True
currentTemperature = 0
currentHumidity = 0
print("Setting Broadcom Mode")
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledTemperatureAlertPin, GPIO.OUT) 
GPIO.setup(ledHumidityAlertPin, GPIO.OUT) 
GPIO.setup(buttonTemperaturePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonHumidityPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Initial button state
#print initial settings
buttonTemperatureState = GPIO.input(buttonTemperaturePin);
print "Initial temperature state is ", 'pressed' if buttonTemperatureState else 'released';
buttonHumidityState = GPIO.input(buttonHumidityPin);
print "Initial temperature state is ", 'pressed' if buttonHumidityState else 'released';

# Initial led state
GPIO.output(ledTemperatureAlertPin, GPIO.LOW)
GPIO.output(ledHumidityAlertPin, GPIO.LOW)

# Initial temperature and humidity
currentHumidity = SHT21(1).read_humidity()
currentTemperature = SHT21(1).read_temperature()
time.sleep(1) 
print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        buttonTemperatureState = GPIO.input(buttonTemperaturePin);
        buttonHumidityState = GPIO.input(buttonHumidityPin);
        if prevTemperatureButtonState != buttonTemperatureState:
            print "Button for temperature is ", 'pressed' if buttonTemperatureState else 'released';
        if prevHumidityButtonState != buttonHumidityState:
            print "Button for humidity is ", 'pressed' if buttonHumidityState else 'released';

            
        # get temperature and humidity
        currentHumidity = SHT21(1).read_humidity()
        currentTemperature = SHT21(1).read_temperature()
        
        print "Temperature: %s" % currentTemperature
        print "Humidity: %s" % currentHumidity
        # Set alerts
        temperatureAlert = currentTemperature > 45
        humidityAlert = currentHumidity < 25 or currentHumidity > 60
        # save last state
        prevTemperatureButtonState = buttonTemperatureState;
        prevHumidityButtonState = buttonHumidityState;
        if temperatureAlert and buttonTemperatureState:
            print ("Threshold met for temperature, LED SHOULD BE ON");            
            GPIO.output(ledTemperatureAlertPin, GPIO.HIGH)
        if not temperatureAlert or not buttonTemperatureState:
            GPIO.output(ledTemperatureAlertPin, GPIO.LOW)
        if humidityAlert and buttonHumidityState:
            print ("Threshold met for humidity, LED SHOULD BE ON");            
            GPIO.output(ledHumidityAlertPin, GPIO.HIGH)
        if not humidityAlert or not buttonHumidityState:
            GPIO.output(ledHumidityAlertPin, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO