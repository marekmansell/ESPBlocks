# This code will blink the NodeMCU's onboard LED
import machine
import time
a = machine.Pin(2, machine.Pin.OUT)
while True:
    time.sleep(1) # Wait 1 second
    a.value(not a.value())