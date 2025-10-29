"""
Connor Chang
ENME441 - Lab 7
Question 2: Instant LED Brightness Control (AJAX)
"""

import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pwms = [] #initialize pwms list
LED_PINS = [17, 27, 22]

#create PWM objects for each LED
for i in LED_PINS:
    GPIO.setup(i, GPIO.OUT)
    pwm_obj = GPIO.PWM(i, 1000) #set 1000Hz freq
    pwm_obj.start(0) #start w/ zero brightness for each pin
    pwms.append(pwm_obj)

#brightness array to track brightness levels
led_brightness = [0, 0, 0]

# helper function to extract key,value pairs of POST data (from lecture)
def parsePOSTdata(data):
    data_dict = {}
    idx = data.find('\r\n\r\n') + 4
    data = data[idx:] # Slice to get only the body data
    data_pairs = data.split('&')
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
    return data_dict

# -----------------------------------
# HTML Page Generator (LLM) - REVISED FOR AJAX
# -----------------------------------
def generate_html():
    """Return a full HTML page showing sliders and using JavaScript/AJAX for updates."""
    
    # 1. Determine the brightness of the default selected LED (LED 1 at index 0)
    # This value is now used to set the initial position of the sliders
    default_slider_value = led_brightness[0]
    
    html = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
<title>Instant LED Brightness Control</title>
<style>
    /* Styling to match the requested interface example */
    body {{ font-family: sans-serif; padding: 20px; }}
    .led-control {{ display: flex; align-items: center; margin-bottom: 15px; border: 1px solid #ccc; padding: 10px; border-radius: 5px; }}
    .led-control label {{ width: 60px; font-weight: bold; }}
    .led-control input[type="range"] {{ flex-grow: 1; margin: 0 15px; }}
    .led-control span {{ width: 30px; text-align: right; font-weight: bold; }}
</style>
</head>
<body>
<h3>Brightness level:</h3>

<div id="controls">
    
    <div class="led-control">
        <label>LED 1</label>
        <input type="range" id="slider0" min="0" max="100" value="{led_brightness[0]}" 
               oninput="updateBrightness(0, this.value)">
        <span id="value0">{led_brightness[0]}</span>
    </div>

    <div class="led-control">
        <label>LED 2</label>
        <input type="range" id="slider1" min="0" max="100" value="{led_brightness[1]}" 
               oninput="updateBrightness(1, this.value)">
        <span id="value1">{led_brightness[1]}</span>
    </div>

    <div class="led-control">
        <label>LED 3</label>
        <input type="range" id="slider2" min="0" max="100" value="{led_brightness[2]}" 
               oninput="updateBrightness(2, this.value)">
        <span id="value2">{led_brightness[2]}</span>
    </div>
    
</div>

<script>
    // JavaScript function to handle slider movement and send AJAX request
    function updateBrightness(ledIndex, brightnessValue) {{
        // 1. Instantly update the displayed value next to the slider on the page
        document.getElementById('value' + ledIndex).innerText = brightnessValue;
        
        // 2. Prepare the data payload in the format the server's parsePOSTdata expects
        const postData = `led=${{ledIndex}}&brightness=${{brightnessValue}}`;
        
        // 3. Use the Fetch API to send a POST request without reloading the page
        fetch(window.location.href, {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/x-www-form-urlencoded',
            }},
            body: postData
        }})
        .then(response => {{
            // Optional: Log successful communication to the console
            if (response.ok) {{
                console.log(`LED ${{ledIndex}} update sent.`);
            }}
        }})
        .catch(error => console.error('AJAX Error:', error));
    }}
</script>

</body>
</html>
"""
    return html
    
# -----------------------------------

HOST = '' #empty string to allow all connections
PORT = 8080 #initialize port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket w/ IPv4 socket and use TCP as the message transport protocol
s.bind((HOST, PORT)) #bind host through given port
s.listen(1) #listen for clients, up to 1 connection

print("Open: http://172.20.10.2:" + str(PORT))

try:
    while True:
        conn, addr = s.accept() #accept client connection
        request = conn.recv(1024).decode('utf-8')
        """
        recieves data from the client with maximum of 1024 bytes
        the network data is decoded and transmitted into raw bytes then back to string
        """
        
        if not request: #close the connection socket and continue to next iteration of while loop if request is empty
            conn.close()
            continue

        #parse the data
        # Check if it's a POST (form submission, now sent by AJAX)
        if request.startswith("POST"):
            data = parsePOSTdata(request)
            
            # Extract and convert the values (which are strings from the POST body)
            try:
                # The keys 'led' and 'brightness' match the JavaScript payload
                led = int(data.get("led", 0))
                new_brightness = int(data.get("brightness", 0))

                # Update hardware and tracking array if data is valid
                if 0 <= led < len(pwms):
                    # Clamp brightness to 0-100 range for safety
                    brightness_clamped = max(0, min(100, new_brightness))
                    
                    led_brightness[led] = brightness_clamped
                    pwms[led].ChangeDutyCycle(brightness_clamped)
                    
            except ValueError:
                print("Error: Received invalid value.")

        #update HTML page w/ LLM function
        # Send back the current HTML page (needed for initial GET, ignored by POST/AJAX)
        response = generate_html()
        conn.sendall(response.encode('utf-8'))
        conn.close()

except KeyboardInterrupt:
    print("\nExiting")

finally:
    #cleanup GPIO and close socket
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup()
    s.close()
