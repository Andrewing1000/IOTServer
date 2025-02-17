import network
import ubinascii
import urequests as requests
from secrets import secrets  # Archivo separado con las credenciales Wi-Fi
import socket
from machine import Pin
import time
import sys
import gc
from utime import sleep

ssid = secrets['ssid']
password = secrets['password']

# Función para inicializar la conexión Wi-Fi
def wifi_init():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)
    wlan.active(True)
    
    while wlan.active() == False:
      pass
    print('Coneccion exitosa')
    print(wlan.ifconfig())

#     print('Esperando encender el modulo wifi...')
#     sleep(3) # wait three seconds for the chip to power up and initialize
#     wlan.connect(ssid, password)       
#     print('Esperando encender el modulo wifi...')
#     sleep(3) # wait three seconds for the chip to power up and initialize
# 
#     while wlan.active() == False:
#       pass
#     print('Coneccion exitosa')
#     print('IP: ', wlan.ifconfig()[0])
#     print('RSSI: ', wlan.status('rssi'))    
#     mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
#     print("MAC:",mac)
#     print("Canal:",wlan.config('channel'))
#     print("SSID:",wlan.config('essid'))
#     print("power:",wlan.config('txpower'))
#     print("Hostname:",wlan.config('hostname'))


# Función para cargar una página HTML desde un archivo
def get_html(html_name):
    try:
        with open(html_name, 'r') as file:
            html = file.read()
        return html
    except Exception as e:
        print(f"Error al leer el archivo {html_name}: {e}")
        return "<html><body>Error al cargar el archivo HTML</body></html>"

