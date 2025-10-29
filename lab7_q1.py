import socket
import RPi.GPIO as GPIO

# Fix: Initialize pwms list
pwms = []

# Helper function to extract key,value pairs of POST data
def parsePOSTdata(data):
    """
    Extracts key/value pairs from the body of a raw HTTP POST request string.
    Expects data in the format: key1=value1&key2=value2...
    """
    data_dict = {}
    # Find the end of the headers and the start of the data body
    # \r\n\r\n is the separator between headers and body
    idx = data.find('\r\n\r\n') + 4
    data = data[idx:] # Slice to get only the body data
    
    # Split the body into individual key=value pairs
    data_pairs = data.split('&')
    
    for pair in data_pairs:
        # Split each pair into key and value
        key_val = pair.split('=')
        # Ensure we have both key and value
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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket w/ IPv4 socket and use TCP as the message transport protocol
server_socket.bind((HOST, PORT)) #bind host through given port
server_socket.listen(1) #listen for clients

print(f"Server running on port {PORT}")
print("Open: http://<172.20.10.2>:" + str(PORT))

try:
    while True:
        conn, addr = server_socket.accept() #accept client connection
        request = conn.recv(1024).decode('utf-8')
        """
        recieves data from the socket object with maximum of 1024 bytes
        the network data is decoded and transmitted into raw bytes then back to string
        """
#close the connection socket and continue to next iteration of while loop if request is empty
        if not request:
            conn.close()
            continue

        # Check if it's a POST (form submission)
        if request.startswith("POST"):
            
            # --- USING THE NEW PARSING FUNCTION ---
            # 1. Call the function to get the form data dictionary
            form_data = parsePOSTdata(request)

            # 2. Extract and convert the values
            # The values from the POST body are strings, so they must be converted to int
            selected_led = int(form_data.get("led", 0))
            new_brightness = int(form_data.get("brightness", 0))

            # Update LED brightness
            led_brightness[selected_led] = new_brightness
            pwms[selected_led].ChangeDutyCycle(new_brightness)

        # Send back the current HTML page
        response = generate_html()
        conn.sendall(response.encode('utf-8'))
        conn.close()

except KeyboardInterrupt:
    print("\nShutting down server...")

finally:
    # Cleanup GPIO and close socket
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup()
    server_socket.close()
