from machine import Pin, PWM, ADC
import network
import socket
import time
import asyncio
import select

mode = 0;
val = 100;
led_3 = PWM(Pin(12, Pin.OUT))
led_2 = PWM(Pin(14, Pin.OUT))
led_1 = PWM(Pin(27, Pin.OUT))

led_1.freq(5000)
led_2.freq(5000)
led_3.freq(5000)

leds = [led_1, led_2, led_3]

button = Pin(15, Pin.IN, pull=Pin.PULL_UP)
pot = ADC(Pin(33, Pin.IN, pull=None))


loading=False
notifing=False
success=False
timeout=4
transition=100
t0=0

wifi = network.WLAN(network.STA_IF)
wifi.active(False)
time.sleep(1)
wifi.active(True)
#res = wifi.scan()
# for e in res:
#     s = ""
#     for x in e:
#         s+= str(x) + " "
#         
#     print(res)



wifi.connect("BLADE", "redminote")
max_wait = 10
while not wifi.isconnected() and max_wait > 0:
    print("Waiting for connection...")
    time.sleep(1)
    max_wait -= 1
    
print(wifi.isconnected())
print(wifi.ifconfig())
addr = socket.getaddrinfo(wifi.ifconfig()[3], 8080)[0][-1]
print(addr)

async def create_request():
    global loading;
    print("...Creando instancia")
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    client.setblocking(False)
    
    try:
        client.connect(addr)
    except OSError as e:
        if e.args[0] != 119:
            client.close()
            raise
    timeout = 5
    start_time = time.time()
    while time.time() - start_time < timeout:
        _, writable, _ = select.select([], [client], [], 0)
        if writable:
            break
        await asyncio.sleep(0.1)

    path = "/tienda/iotinterface/"
    request = f"POST {path} HTTP/1.1\r\n"
    request += f"Host: {addr[0]}\r\n"
    request += "Content-Type: application/json\r\n"
    request += "Content-Length: 0\r\n"
    request += f"CEBOLLIN: {wifi.ifconfig()[0]}\r\n"
    request += "Connection: close\r\n\r\n"
        
    success = False
    while abs(time.time()-t0)<timeout:
        if not loading: break
        try:  
            client.send(request.encode())
            success = True
            break
        except OSError as e:
            if e.args[0] == 119:
                await asyncio.sleep(0.1)
                
    if not success:
        return success
    
    response = b""            
    while True:
        try:
            chunk = client.recv(4096)  
            if not chunk:
                break
            response += chunk
        except OSError as e:
            if e.args[0] == 11: 
                await asyncio.sleep(0.1)
            else:
                raise                 
                
    response = response.decode()
    loading = False
    client.close()
    return response


async def delete_request():
    global loading
    print("...Eliminando instancia")
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    client.setblocking(False)
    
    try:
        client.connect(addr)
    except OSError as e:
        if e.args[0] != 119:
            client.close()
            raise
    timeout = 5
    start_time = time.time()
    while time.time() - start_time < timeout:
        _, writable, _ = select.select([], [client], [], 0)
        if writable:
            break
        await asyncio.sleep(0.1)

    path = "/tienda/iotinterface/"
    request = f"DELETE {path} HTTP/1.1\r\n"
    request += f"Host: {addr[0]}\r\n"
    request += "Connection: close\r\n"
    request += f"CEBOLLIN: {wifi.ifconfig()[0]} \r\n\r\n"
    
    success = False
    while abs(time.time()-t0)<timeout:
        if not loading: break
        try:  
            client.send(request.encode())
            success = True
            break
        except OSError as e:
            if e.args[0] == 119:
                await asyncio.sleep(0.1)
             
    if not success:
        return success
    
    response = b""              
    while True:
        try:
            chunk = client.recv(4096)
            if not chunk:
                break
            response += chunk
        except OSError as e:
            if e.args[0] ==11:
                asyncio.sleep(0.1)
            else:
                raise
         
    response = response.decode()
    loading = False                
    client.close()
    return response
    

click = asyncio.Event()
cooldown = 50
last_click = 0
def switch_mode(pin):
    global loading, t0, last_click
    if abs(last_click-time.time())*1000 < cooldown:
        return
    loading = True
    t0=time.time()
    last_click = time.time()
    click.set()

pot.atten(ADC.ATTN_11DB)
button.irq(trigger=Pin.IRQ_FALLING, handler=switch_mode)

async def refresh():
    global loading, mode, notifing
    while(True):
        mode = int(pot.read()*1.9999/4095)
        for led in leds:
            led.duty(0)
        leds[mode].duty(val)
        
        while(loading):
            leds[mode].duty(val)
            led_3.duty(val)
            await asyncio.sleep(transition/1000)
            led_3.duty(0)
            await asyncio.sleep(transition/1000)
            
        await asyncio.sleep(0)        

def get_status(res):
    status_line = res.splitlines()[0]
    status = int(status_line.split(" ")[1])
    return status
            
def get_body(res):
    sta = res.split("\r\n\r\n")
    return sta[-1]
    
async def request():
    global notifing
    global success
    while(True):
        await click.wait()
        res = None
        success = False
        if mode == 0:
            res = await create_request()
            status = get_status(res)
            print("--------------------------------")
            if not res:
                print("Error de conección")
            elif(status!=200):
                print("Error interno")
            else:
                success = True
                print("Creación exitosa")
                print(get_body(res))
            
        else:
            res = await delete_request()
            status = get_status(res)
            print("--------------------------------")
            if not res:
                print("Error de conección")
            elif(status!=200):
                print("Error interno")
                print(get_body(res))
            else:
                success = True
                print("Eliminación exitosa")
         
        click.clear()        
        await asyncio.sleep(0)
    

async def main():
    await asyncio.gather(request(), refresh())
    
asyncio.run(main())


