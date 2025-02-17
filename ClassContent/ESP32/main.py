import sys
import os
import network
import ubinascii
import machine
from machine import Pin
import urequests as requests
import time
import random
import socket
import sys
from secrets import secrets  # Archivo separado para las credenciales Wi-Fi
from Wifi_lib import wifi_init, get_html  # Librerías externas

# Configuración inicial
led_state = "@@"
random_value = 0

# Inicializar la conexión Wi-Fi
wifi_init()
# Detectando el tipo de tarjeta 
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
print("Tarjeta Detectada: " + BOARD_TYPE)

# Configuración de los pines según la tarjeta detectada
if BOARD_TYPE == Board.BoardType.PICO_W:
    led = Pin("LED", Pin.OUT)  # LED interno para Raspberry Pi Pico W
elif BOARD_TYPE == Board.BoardType.PICO or BOARD_TYPE == Board.BoardType.RP2040:
    led = Pin(25, Pin.OUT)  # LED interno para Raspberry Pi Pico o RP2040
elif BOARD_TYPE == Board.BoardType.ESP8266:
    led = Pin(12, Pin.OUT)  # GPIO 2 para el ESP8266 (LED interno)
elif BOARD_TYPE == Board.BoardType.ESP32:
    led = Pin(14, Pin.OUT)  # GPIO 2 para el ESP32 (LED integrado)
else:
    print("Placa desconocida, usando GPIO 2 por defecto.")
    led = Pin(2, Pin.OUT)  # Pin por defecto para placas desconocidas    


# Configuración del servidor HTTP con sockets
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Servidor escuchando en:', addr)

# Bucle para escuchar conexiones
while True:
    try:
        cl, addr = s.accept()
        print('Cliente conectado desde', addr)
        request = cl.recv(1024)
        request = str(request)

        # Procesar la solicitud HTTP
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        valor = request.find('value')

        print('led_on  =', led_on)
        print('led_off =', led_off)
        print('valor   =', valor)

        # Encender o apagar el LED según la solicitud
        if led_on > -1:
            print('LED ENCENDIDO')
            led.value(1)
            led_state = "ON"
        elif led_off > -1:
            print('LED APAGADO')
            led.value(0)
            led_state = "OFF"

        # Generar un valor aleatorio si se solicita
        if valor > -1:
            random_value = random.randint(0, 20)

        # Obtener y personalizar la respuesta HTML
        response = get_html('index.html')
        response = response.replace('led_state', led_state)
        response = response.replace('random_value', str(random_value))

        # Enviar la respuesta al cliente
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('Conexión cerrada debido a un error:', e)
