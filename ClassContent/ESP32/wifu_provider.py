import socket
import network
#from secrets import secret
#importing network
#import gc
#gc.collect()
ssid = 'Latomy'                  #Set access point name 
password = 'VtuberGG'      #Set your access point password

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)
ap.active(True)            #activating

while ap.active() == False:
  pass
print('Coneccion exitosa')
print(ap.ifconfig())
def web_page():
  html = """<!DOCTYPE html>
    <html>
        <head> <title>Pico W ESP32</title> </head>
        <body>
            <h1>Pico W ESP32</h1>
            <h2> Internet de las Cosas </h2>
            <p>         SIS 234           </p>
            <h3>HOLA MUNDO!! PSV</h3>
        </body>
    </html>
    """
  return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
s.bind(('', 80))
s.listen(5)
while True:
  conn, addr = s.accept()
  print('Coneccion establecida de %s' % str(addr))
  request = conn.recv(1024)
  print('Respuesta = %s' % str(request))
  response = web_page()
  conn.send(response)
  conn.close()