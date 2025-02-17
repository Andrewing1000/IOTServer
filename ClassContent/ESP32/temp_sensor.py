import sys
import os
from machine import Pin
import time
import dht

class Board:
    class BoardType:
        PICO_W = 'Raspberry Pi Pico W'
        PICO = 'Raspberry Pi Pico'
        RP2040 = 'RP2040'
        ESP8266 = 'ESP8266'
        ESP32 = 'ESP32'
        UNKNOWN = 'Unknown'

    def __init__(self):
        self.type = self.detect_board_type()

    def detect_board_type(self):
        sysname = os.uname().sysname.lower()
        machine = os.uname().machine.lower()

        # Detectar Raspberry Pi Pico W y Pico
        if sysname == 'rp2' and 'pico w' in machine:
            return self.BoardType.PICO_W
        elif sysname == 'rp2' and 'pico' in machine:
            return self.BoardType.PICO
        elif sysname == 'rp2' and 'rp2040' in machine:
            return self.BoardType.RP2040

        # Detectar ESP8266
        elif sysname == 'esp8266':
            return self.BoardType.ESP8266

        # Detectar ESP32
        elif sysname == 'esp32' and 'esp32' in machine:
            return self.BoardType.ESP32

        # Desconocido
        else:
            return self.BoardType.UNKNOWN

# Detectar tipo de placa
BOARD_TYPE = Board().type
print("Tipo de placa: " + BOARD_TYPE)

# Configuración de los pines según la tarjeta detectada
if BOARD_TYPE == Board.BoardType.PICO_W:
    led = Pin("LED", Pin.OUT)  # LED interno para Raspberry Pi Pico W
    data_pin = 16              # Pin de datos para el sensor DHT22
elif BOARD_TYPE == Board.BoardType.PICO or BOARD_TYPE == Board.BoardType.RP2040:
    led = Pin(25, Pin.OUT)     # LED interno para Raspberry Pi Pico o RP2040
    data_pin = 16              # Pin de datos para el sensor DHT22
elif BOARD_TYPE == Board.BoardType.ESP8266:
    led = Pin(2, Pin.OUT)      # GPIO 2 para el ESP8266 (LED interno)
    data_pin = 0               # Pin de datos para el sensor DHT22 en ESP8266
elif BOARD_TYPE == Board.BoardType.ESP32:
    led = Pin(2, Pin.OUT)      # GPIO 2 para el ESP32 (LED integrado)
    data_pin = 4               # Pin de datos para el sensor DHT22 en ESP32
else:
    print("Placa desconocida, usando GPIO 2 y pin de datos 0 por defecto.")
    led = Pin(2, Pin.OUT)      # Pin por defecto para LED
    data_pin = 0               # Pin de datos por defecto para el DHT22

# Configuración del sensor DHT22
dht_sensor = dht.DHT22(Pin(data_pin))

# Umbrales de temperatura y humedad
umbral_temperatura = 30.0  # Ajusta el valor según tus necesidades
umbral_humedad = 40.0      # Ajusta el valor según tus necesidades

def leer_dht22():
    # Leer el sensor y obtener la temperatura y humedad
    dht_sensor.measure()
    temperatura = dht_sensor.temperature()
    humedad = dht_sensor.humidity()
    return temperatura, humedad

def controlar_led(temperatura, humedad):
    # Encender el LED si la temperatura o la humedad superan los umbrales
    if temperatura > umbral_temperatura or humedad > umbral_humedad:
        led.on()  # Enciende el LED
        print("Alta temperatura o humedad, LED encendido")
    else:
        led.off()  # Apaga el LED
        print("Temperatura y humedad normales, LED apagado")

while True:
    # Leer la temperatura y humedad y controlar el LED
    try:
        temperatura, humedad = leer_dht22()
        print("Temperatura DHT22: {:.2f}°C, Humedad: {:.2f}%".format(temperatura, humedad))
        controlar_led(temperatura, humedad)
    except OSError as e:
        print("Error al leer el sensor DHT22:", e)
    
    # Espera de dos segundos antes de la siguiente lectura
    time.sleep(1)
