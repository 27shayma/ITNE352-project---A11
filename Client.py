import socket
import PySimpleGUI as psg
import signal
import sys

# Theme for the PySimpleGUI windows
psg.theme('TealMono')

# Functions
# Creation Function: To create a PySimpleGUI window with a specific title & layout
def Creation(title, layout):
    window= psg.Window(title, layout, resizable=True)
    return window

# ShowF Function: To display data in the PySimpleGUI window
def ShowF(title, data):
    layout = [
        [psg.Text("*"*10 + title + "*"*10, font=('Arial',12, 'bold'))],
        [psg.Column([[psg.Text(data, font=('Arial',10))]], scrollable=True)],
        [psg.Button('OK')]
    ]
    window = Creation(title, layout)
    event, value = window.read()
    window.close()

# Signal_Handler Function: To handle the Ctrl+C signal with by sending a termination message
def Signal_Handler(sig, frame):
    termination_message = "User is terminating the connection"
    client_socket.send(termination_message.encode("utf-8"))
    client_socket.close()
    sys.exit(0)

# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, Signal_Handler)

# Input_Window Function: To create an input window & handle the user's input
def Input_Window (title, layout):
    window = Creation(title, layout)
    while True:
        event, values = window.read()
        if event in (psg.WINDOW_CLOSED, 'Cancel'):
            window.close()
            return None
        if values['-INPUT-']:
            input=values['-INPUT-']
            window.close()
            return input

# Socket is created
client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step one: establishing the connection to the server
server_ip = '127.0.0.2'
server_port = 55555

# Exception Handling
try:
    # Establishes a connection to the server
    client_socket.connect((server_ip, server_port))
    print("Connected to the server.")
except ConnectionRefusedError:
    psg.PopupError("Connection refused. Make sure the server is running.")
    exit()
except Exception as e:
    print(f"An error occurred while connecting to the server: {e}")
    exit()

# User is prompted to enter their username
username_layout = [
    [psg.Text("Please enter your username: ", font=("Arial Bold", 14))],
    [psg.Input(key="-INPUT-", font=("Arial", 12))],
    [psg.Submit(),psg.Cancel()]
]

# User is prompted to enter their API key
api_key_layout = [
    [psg.Text("Please enter your NewsAPI.org API key: ", font=("Arial Bold", 14))],
    [psg.Input(key="-INPUT-", font=("Arial", 12))],
    [psg.Submit(),psg.Cancel()]
]

# User is prompted to enter the country code
country_code_layout = [
    [psg.Text("Please enter the country code (2-letter ISO 3166-1 format): ", font=("Arial Bold", 14))],
    [psg.Input(key="-INPUT-", font=("Arial", 12))],
    [psg.Submit(),psg.Cancel()]
]

# User is prompted to enter their API key
api_key = Input_Window("API Key", api_key_layout)

# User is prompted to enter the country code
country_code = Input_Window("Country Code", country_code_layout)

# The inserted API key is sent to the server
client_socket.send(api_key.encode('utf-8'))

# The inserted country codeis sent to the server
client_socket.send(country_code.encode('utf-8'))

# User is prompted to enter their username
user = Input_Window("Username", username_layout)

# The inserted username is sent to the server
client_socket.send((user).encode('utf-8'))

# Infinite loop to handle the user's options.
while True:
    options_layout = [
        [psg.Text("Choose one of the following options: ",font=("Arial", 12))],
        [psg.Text("1. Top Headlines",font=("Arial", 12))],
        [psg.Text("2. Sources",font=("Arial", 12))],
        [psg.Text("3. Quit",font=("Arial", 12))],
        [psg.Text('Choose a number between 1-3:',font=("Arial Bold", 14)), psg.Input(key="-INPUT-",font=("Arial", 14))],
        [psg.Button('Send'), psg.Button('Cancel')]
    ]

# User is prompted to choose from the options listed
    option= Input_Window('Options', options_layout)

# The option selected is sent to the server
    client_socket.send((option).encode('utf-8'))

# Top headlines are displayed
    if option == '1':
        data = client_socket.recv(20480).decode("utf-8")
        ShowF('Top Headlines', data)

# Sources are displayed
    elif option == '2':
        data = client_socket.recv(20480).decode("utf-8")
        ShowF('Sources', data)

# The user is prompted to enter their API key
    elif option == "3":
        client_socket.send((user + " is disconnected").encode("utf-8"))
        print("Quitting...")
        client_socket.close()
        psg.popup("Connection terminated.")
        print("Connection terminated!")
        sys.exit(0)