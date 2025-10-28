import socket
# You will also need to import your GPIO library (e.g., RPi.GPIO or pigpio)
import threading

HOST = ''  # Allows any incoming connection
PORT = 8080 # Use a non-privileged port to avoid 'sudo'
LED_STATES = [0, 0, 0] # List to store brightness (0-100) for LED 1, 2, 3

# Example structure for handling a single request in a thread (similar to webserver_threaded.py)
def handle_client(conn):
    request = conn.recv(1024).decode()

    # Check if it's a POST request (starts with "POST / HTTP/1.1")
    # If POST, parse the data, update LED_STATES, and then generate the HTML
    # If GET (for initial page load), just generate the HTML

    # Update LED state logic here (using your GPIO library)
    # ...

    response_html = generate_html() # Call function to build the HTML page

    # Send HTTP Response
    conn.send(b'HTTP/1.1 200 OK\r\n')
    conn.send(b'Content-type: text/html\r\n')
    conn.send(b'Connection: close\r\n\r\n')
    conn.sendall(response_html.encode())
    conn.close()

def run_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1) # Listen for up to 1 queued connection
    while True:
        conn, addr = s.accept() # Blocking call to wait for a connection
        # Start a new thread for each connection to avoid blocking the server
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

# Your main code starts run_server in a thread and continues other tasks
# server_thread = threading.Thread(target=run_server)
# server_thread.start()

<form action="/" method="POST">
    <h2>Brightness level:</h2>
    <input type="range" name="value" min="0" max="100" value="50"><br>
    
    <h2>Select LED:</h2>
    <input type="radio" name="led_select" value="1" checked> LED 1 (0%) <br>
    <input type="radio" name="led_select" value="2"> LED 2 (0%) <br>
    <input type="radio" name="led_select" value="3"> LED 3 (0%) <br><br>

    <button type="submit">Change Brightness</button>
</form>
