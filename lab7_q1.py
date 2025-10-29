import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

LED_PINS = [17, 27, 22]

#create PWM objects for each LED
pwm = []
for i in LED_PINS:
    GPIO.setup(i, GPIO.OUT)
    pwm = GPIO.PWM(i, 1000) #set 1000Hz freq
    pwm.start(0) #start w/ zero brightness for each pun
    pwms.append(pwm)

#brightness array to track brightness levels
led_brightness = [0, 0, 0]


# -----------------------------------
# HTML Page Generator
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
# TCP/IP Web Server
# -----------------------------------
HOST = ''   # Listen on all available interfaces
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server running on port {PORT}...")
print("Open a browser and go to: http://<your_pi_ip>:" + str(PORT))

try:
    while True:
        conn, addr = server_socket.accept()
        request = conn.recv(1024).decode('utf-8')

        # Debug print
        # print("Request:\n", request)

        if not request:
            conn.close()
            continue

        # Check if it's a POST (form submission)
        if request.startswith("POST"):
            # Extract body (data after the blank line)
            body = request.split("\r\n\r\n")[1]
            form_data = dict(param.split('=') for param in body.split('&'))

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
