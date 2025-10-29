import socket
import RPi.GPIO as GPIO

pwms = [] #initialize pwms list

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

GPIO.setmode(GPIO.BCM)

LED_PINS = [17, 27, 22]

#create PWM objects for each LED
for i in LED_PINS:
    GPIO.setup(i, GPIO.OUT)
    pwm_obj = GPIO.PWM(i, 1000) #set 1000Hz freq
    pwm_obj.start(0) #start w/ zero brightness for each pin
    pwms.append(pwm_obj)

#brightness array to track brightness levels
led_brightness = [0, 0, 0]


# -----------------------------------
# HTML Page Generator (LLM)
# -----------------------------------
def generate_html():
    """Return a full HTML page showing sliders, radio buttons, and LED states."""
    
    # 1. Determine the brightness of the default selected LED (LED 1 at index 0)
    default_slider_value = led_brightness[0]
    
    html = f"""\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
<title>LED Brightness Control</title>
</head>
<body>
<h3>Brightness level:</h3>

<form method="POST">
<input type="range" name="brightness" min="0" max="100" value="{default_slider_value}"><br><br>

<b>Select LED:</b><br>
<input type="radio" name="led" value="0" checked> LED 1 ({led_brightness[0]}%)<br>
<input type="radio" name="led" value="1"> LED 2 ({led_brightness[1]}%)<br>
<input type="radio" name="led" value="2"> LED 3 ({led_brightness[2]}%)<br><br>

<input type="submit" value="Change Brightness">
</form>

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
            led = int(data.get("led", 0))
            new_brightness = int(data.get("brightness", 0))
            led_brightness[led] = new_brightness
            pwms[led].ChangeDutyCycle(new_brightness)

        #update HTML page w/ LLM function
        response = generate_html()
        conn.sendall(response.encode('utf-8'))

except KeyboardInterrupt:
    print("\nExiting")

finally:
    #cleanup GPIO and close socket
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup()
    s.close()
