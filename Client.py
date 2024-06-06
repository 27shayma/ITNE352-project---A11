import socket
import json
import PySimpleGUI as sg

class NewsClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
        except ConnectionRefusedError:
            sg.popup_error('Unable to connect to the server. Please make sure the server is running.')
            exit()

    def send_request(self, request):
        try:
            self.sock.sendall(json.dumps(request).encode())
            response = self.sock.recv(4096).decode()
            return json.loads(response)
        except socket.error as e:
            sg.popup_error(f'Socket error: {e}')
            return None

    def close_connection(self):
        try:
            self.sock.sendall("QUIT".encode())
            self.sock.close()
        except socket.error as e:
            sg.popup_error(f'Socket error while closing connection: {e}')

def display_results(results, title):
    layout = [[sg.Text(f"{title}", size=(50, 1), justification='center', font=('Helvetica', 16))]]
    if isinstance(results, list) and len(results) > 0:
        for result in results:
            layout.append([sg.Text(f"{result}")])
    else:
        layout.append([sg.Text("No results found.")])
    layout.append([sg.Button('Back to the main menu')])
    window = sg.Window('Results', layout)
    while True:
        event, values = window.read()
        if event == 'Back to the main menu' or event == sg.WINDOW_CLOSED:
            window.close()
            break

def main():
    client_name = sg.popup_get_text('Enter your name')
    if not client_name:
        return

    client = NewsClient()
    client.sock.sendall(client_name.encode())

    main_menu = [
        [sg.Button('Search headlines')],
        [sg.Button('List of Sources')],
        [sg.Button('Quit')]
    ]

    headlines_menu = [
        [sg.Button('Search for keywords')],
        [sg.Button('Search by category')],
        [sg.Button('Search by country')],
        [sg.Button('List all new headlines')],
        [sg.Button('Back to the main menu')]
    ]

    sources_menu = [
        [sg.Button('Search by category')],
        [sg.Button('Search by country')],
        [sg.Button('Search by language')],
        [sg.Button('List all')],
        [sg.Button('Back to the main menu')]
    ]

    layout = [
        [sg.Text('Main Menu', size=(30, 1), justification='center')],
        [sg.Column(main_menu, key='-MAIN-'), 
         sg.Column(headlines_menu, visible=False, key='-HEADLINES-'), 
         sg.Column(sources_menu, visible=False, key='-SOURCES-')]
    ]

    window = sg.Window('News Client', layout, finalize=True)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Quit'):
            client.close_connection()
            break

        if event == 'Search headlines':
            window['-MAIN-'].update(visible=False)
            window['-HEADLINES-'].update(visible=True)
            window['-SOURCES-'].update(visible=False)

        elif event == 'List of Sources':
            window['-MAIN-'].update(visible=False)
            window['-HEADLINES-'].update(visible=False)
            window['-SOURCES-'].update(visible=True)

        elif event == 'Back to the main menu':
            window['-MAIN-'].update(visible=True)
            window['-HEADLINES-'].update(visible=False)
            window['-SOURCES-'].update(visible=False)

        else:
            option_map = {
                'Search for keywords': 'headlines',
                'Search by category': 'headlines',
                'Search by country': 'headlines',
                'List all new headlines': 'headlines',
                'Search by category': 'sources',
                'Search by country': 'sources',
                'Search by language': 'sources',
                'List all': 'sources'
            }

            option = option_map.get(event)
            if option:
                parameters = {}
                if event == 'Search for keywords':
                    keyword = sg.popup_get_text('Enter keyword')
                    if keyword:
                        parameters['q'] = keyword
                elif event == 'Search by category':
                    category = sg.popup_get_text('Enter category')
                    if category:
                        parameters['category'] = category
                elif event == 'Search by country':
                    country = sg.popup_get_text('Enter country')
                    if country:
                        parameters['country'] = country
                elif event == 'Search by language':
                    language = sg.popup_get_text('Enter language')
                    if language:
                        parameters['language'] = language

                request = {'option': option, 'parameters': parameters}
                results = client.send_request(request)

                if results is not None:
                    display_results(results, event)

    window.close()

if __name__ == "__main__":
    main()
