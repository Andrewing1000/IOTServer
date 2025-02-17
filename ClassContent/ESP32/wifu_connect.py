import network
import time
import ubinascii
from utime import sleep

ssid = "Latom"
password = "PinchesPeruanos" 

wlan = network.WLAN(network.STA_IF)
wlan.active(True) # power up the WiFi chip
print('Esperando encender el modulo wifi...')
sleep(3) # wait three seconds for the chip to power up and initialize
wlan.connect(ssid, password)       
print('Esperando encender el modulo wifi...')
sleep(3) # wait three seconds for the chip to power up and initialize

while wlan.active() == False:
  pass
print('Coneccion exitosa')
print('IP: ', wlan.ifconfig()[0])
print('RSSI: ', wlan.status('rssi'))    
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print("MAC:",mac)
print("Canal:",wlan.config('channel'))
print("SSID:",wlan.config('essid'))
print("power:",wlan.config('txpower'))
print("Hostname:",wlan.config('hostname'))
