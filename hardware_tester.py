import time
from machine import Pin

# Initialize the button on GP15 with an internal pull-up resistor
button = Pin(15, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

print("--- Button Hardware Tester ---")
print("Press and hold your physical button...")

while True:
    # Read the current physical state of the pin
    pin_value = button.value()
    
    if pin_value == 0:
        print("Button Detected! Status: CLOSED (Pressed)")
        led.on()  # Turn on the onboard LED when pressed
    else:
        led.off() # Keep it off when released
        
    time.sleep(0.1) # Check 10 times a second
