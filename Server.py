import socket
import threading
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure NewsAPI
API_KEY = '0d60857c824e4547903db558a42f7865'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'
NEWS_SOURCES_URL = 'https://newsapi.org/v2/sources'


class NewsServer:
    def __init__(self, group_id):
        self.group_id = group_id
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', 5555))
        self.server.listen(5)
        logging.info("[STARTING] Server is starting...")

    def handle_client(self, client_socket, client_address):
        logging.info(f"[CONNECTION] Client {client_address} connected.")
        try:
            client_name = client_socket.recv(1024).decode('utf-8')
            logging.info(f"[CLIENT NAME] {client_name} connected.")

            while True:
                request = client_socket.recv(1024).decode('utf-8')
                if not request or request.lower() == 'quit':
                    logging.info(f"[DISCONNECT] Client {client_name} disconnected.")
                    break

                response = self.process_request(request)
                filename = f"{self.group_id}_{client_name}_{request.split('?')[0]}.json"
                with open(filename, 'w') as f:
                    json.dump(response, f, indent=4)

                client_socket.send(json.dumps(response).encode('utf-8'))
        except ConnectionResetError:
            logging.error(f"[ERROR] Connection lost with {client_address}")
        finally:
            client_socket.close()

    def process_request(self, request):
        if request.startswith('headlines'):
            return self.get_news(NEWS_API_URL, request.split('?')[1] if '?' in request else '')
        elif request.startswith('sources'):
            return self.get_news(NEWS_SOURCES_URL, request.split('?')[1] if '?' in request else '')
        else:
            return {'error': 'Invalid request'}

    def get_news(self, url, params):
        try:
            params_dict = {param.split('=')[0]: param.split('=')[1] for param in params.split('&') if param}
            params_dict['apiKey'] = NEWS_API_KEY
            response = requests.get(url, params=params_dict)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error fetching news data: {e}")
            return {"error": "Failed to fetch news data"}

    def start(self):
        while True:
            client_socket, client_address = self.server.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_handler.start()

if __name__ == "__main__":
    server = NewsServer("A11")
    server.start()