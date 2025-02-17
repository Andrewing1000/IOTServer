from machine import Pin, PWM, ADC
import time

mode = 0;
val = 1023;

def switch_mode(pin):
    global mode
    mode = (mode+1)%3
    print(mode)


led_1 = PWM(Pin(12, Pin.OUT))
led_2 = PWM(Pin(14, Pin.OUT))
led_3 = PWM(Pin(27, Pin.OUT))

led_1.freq(5000)
led_2.freq(5000)
led_3.freq(5000)

leds = [led_1, led_2, led_3]

button = Pin(15, Pin.IN, pull=Pin.PULL_UP)
pot = ADC(Pin(26, Pin.IN, pull=None))

button.irq(trigger=Pin.IRQ_FALLING, handler=switch_mode)

def refresh():
    for led in leds:
        led.duty(0)
        
#     for i in range(0, 3):
#         if((mode>>i)&1 == 1):
#             print(i)
    
    leds[mode].duty(val)



while(True):
    #val = int(pot.read()*1023/4095)
    mode = int(pot.read()*2/4095)
    #print(mode)
    refresh()
    #print(val, pot.read())
    time.sleep(0.100)