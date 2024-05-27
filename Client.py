import socket
import PySimpleGUI as psg
import signal
import sys

psg.theme('TealMono')

def Creation(title, layout):
    window = psg.Window(title, layout, resizable=True)
    return window

def ShowF(title, data):
    layout = [
        [psg.Text("" * 10 + title + "" * 10, font=('Arial', 12, 'bold'))],
        [psg.Column([[psg.Text(data, font=('Arial', 10))]], scrollable=True)],
        [psg.Button('OK')]
    ]
    window = Creation(title, layout)
    event, value = window.read()
    window.close()

def Signal_Handler(sig, frame):
    termination_message = "User is terminating the connection"
    client_socket.send(termination_message.encode("utf-8"))
    client_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, Signal_Handler)

def Input_Window(title, layout):
    window = Creation(title, layout)
    while True:
        event, values = window.read()
        if event in (psg.WINDOW_CLOSED, 'Cancel'):
            window.close()
            return None
        if values['-INPUT-']:
            input_value = values['-INPUT-']
            window.close()
            return input_value

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = '127.0.0.1'
server_port = 12345

try:
    client_socket.connect((server_ip, server_port))
    print("Connected to the server.")
except ConnectionRefusedError:
    psg.PopupError("Connection refused. Make sure the server is running.")
    exit()
except Exception as e:
    print(f"An error occurred while connecting to the server: {e}")
    exit()

username_layout = [
    [psg.Text("Please enter your username: ", font=("Arial Bold", 14))],
    [psg.Input(key="-INPUT-", font=("Arial", 12))],
    [psg.Submit(), psg.Cancel()]
]

api_key_layout = [
    [psg.Text("Please enter your NewsAPI.org API key: ", font=("Arial Bold", 14))],
    [psg.Input(key="-INPUT-", font=("Arial", 12))],
    [psg.Submit(), psg.Cancel()]
]

country_code_layout = [
    [psg.Text("Please enter the country code (2-letter ISO 3166-1 format): ", font=("Arial Bold", 14))],
    [psg.Input(key="-INPUT-", font=("Arial", 12))],
    [psg.Submit(), psg.Cancel()]
]

api_key = Input_Window("API Key", api_key_layout)
if not api_key:
    client_socket.close()
    exit()

country_code = Input_Window("Country Code", country_code_layout)
if not country_code:
    client_socket.close()
    exit()

client_socket.send(api_key.encode('utf-8'))
client_socket.send(country_code.encode('utf-8'))

user = Input_Window("Username", username_layout)
if not user:
    client_socket.close()
    exit()

client_socket.send(user.encode('utf-8'))

while True:
    options_layout = [
        [psg.Text("Choose one of the following options: ", font=("Arial", 12))],
        [psg.Text("1. Top Headlines", font=("Arial", 12))],
        [psg.Text("2. Sources", font=("Arial", 12))],
        [psg.Text("3. Quit", font=("Arial", 12))],
        [psg.Text('Choose a number between 1-3:', font=("Arial Bold", 14)), psg.Input(key="-INPUT-", font=("Arial", 14))],
        [psg.Button('Send'), psg.Button('Cancel')]
    ]

    option = Input_Window('Options', options_layout)
    if not option:
        client_socket.send((user + " is disconnected").encode('utf-8'))
        print("Quitting...")
        client_socket.close()
        psg.popup("Connection terminated.")
        print("Connection terminated!")
        break

    client_socket.send(option.encode('utf-8'))

    try:
        if option == '1':
            data = client_socket.recv(20480).decode('utf-8')
            ShowF('Top Headlines', data)

        elif option == '2':
            data = client_socket.recv(20480).decode('utf-8')
            ShowF('Sources', data)

        elif option == '3':
            client_socket.send((user + " is disconnected").encode('utf-8'))
            print("Quitting...")
            client_socket.close()
            psg.popup("Connection terminated.")
            print("Connection terminated!")
            break

    except ConnectionAbortedError:
        psg.PopupError("An error occurred: Connection aborted by the server.")
        print("An error occurred: Connection aborted by the server.")
        client_socket.close()
        break