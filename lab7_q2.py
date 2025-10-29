"""
Connor Chang
ENME441 - Lab 7
Question 2
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
    default_slider_value = led_brightness[0]
    
    html = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
<title>Instant LED Brightness Control</title>
<style>
    body {{ font-family: sans-serif; padding: 20px; }}
    .led-control {{ display: flex; align-items: center; margin-bottom: 15px; }}
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
    // This function sends a POST request with the new LED index and brightness value
    function updateBrightness(ledIndex, brightnessValue) {{
        // Update the displayed value instantly on the client side
        document.getElementById('value' + ledIndex).innerText = brightnessValue;
        
        // Prepare data in the format the server expects: key=value&...
        const postData = `led=${{ledIndex}}&brightness=${{brightnessValue}}`;
        
        // Send AJAX POST request using the Fetch API
        fetch(window.location.href, {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/x-www-form-urlencoded',
            }},
            body: postData
        }});
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
        if request.startswith("POST"):
            data = parsePOSTdata(request)
            
            #extract and convert the values
            try:
                led = int(data.get("led", 0))
                new_brightness = int(data.get("brightness", 0))

                #update led and tracking array if data is valid
                if 0 <= led < len(pwms):
                    led_brightness[led] = new_brightness
                    pwms[led].ChangeDutyCycle(new_brightness)
                    
            except ValueError:
                print("Error: Received invalid value.")
            except Exception as e:
                print(f"Hardware Error: {e}")

        #update HTML page w/ LLM function
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
