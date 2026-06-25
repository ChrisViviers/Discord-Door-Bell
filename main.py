import time
import network
import urequests
import ujson
from machine import Pin

# --- CONFIGURATION ---
WIFI_SSID = "Your_WiFi_Name"
WIFI_PASS = "Your_WiFi_Password"

# Discord Bot Credentials
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
CHANNEL_ID = "YOUR_TARGET_CHANNEL_ID_HERE"

BUTTON_PIN = 15
# ---------------------

# Hardware Setup
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

def connect_wifi():
    """Handles connecting to the local 2.4GHz Wi-Fi network network loop."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        
        # Blink the onboard LED while attempting to authenticate
        while not wlan.isconnected():
            led.toggle()
            time.sleep(0.1)
            
    print("Connected! IP:", wlan.ifconfig()[0])
    led.on() # Solid LED means fully online and ready

def send_bot_message():
    """Formulates and fires a strict, non-chunked JSON payload to Discord."""
    print("Button pressed! Firing Discord Bot API...")
    led.off() # Flash the LED off to indicate data transmission
    
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    
    payload = {
        "content": "🚀 **Alert from the physical world:** The Pico W button was pressed!"
    }
    
    # MicroPython quirk fix: Explicitly serialize to bytes to measure length
    json_bytes = ujson.dumps(payload).encode('utf-8')
    
    # Discord requires Content-Length header to bypass chunked data rejections
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json",
        "Content-Length": str(len(json_bytes))
    }
    
    try:
        response = urequests.post(url, data=json_bytes, headers=headers, timeout=5)
        print("Discord Response Status:", response.status_code)
        
        # Output any API error text directly to the Thonny console
        if response.status_code != 200:
            print("Response Body:", response.text)
            
        response.close() # Always close network sockets
    except Exception as e:
        print("API or Network Error:", e)
        connect_wifi() # Refresh the Wi-Fi connection state if it dropped
        
    led.on()

# Establish initial network connection
connect_wifi()
print("Bot listener active. Awaiting input...")

# Main Execution Loop
last_press = 0
while True:
    # Button reads 0 (LOW) when pressed because it connects directly to GND
    if button.value() == 0:
        current_time = time.ticks_ms()
        
        # Software debouncing: ensure 2 seconds have passed between allowed pings
        if time.ticks_diff(current_time, last_press) > 2000:
            send_bot_message()
            last_press = current_time
            
    time.sleep(0.05) # Tiny script sleep to prevent core throttling
