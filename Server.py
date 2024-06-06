import socket
import threading
import json
import requests
from datetime import datetime

API_KEY = '366c79feda1a41a1a380f1feb8ca4d42'
GROUP_ID = 'A11'

class NewsServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.clients = {}

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("Server started. Waiting for clients...")
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        client_name = client.recv(1024).decode()
        self.clients[client_name] = client
        print(f"Client {client_name} connected.")
        try:
            while True:
                request = client.recv(1024).decode()
                if request == "QUIT":
                    print(f"Client {client_name} disconnected.")
                    del self.clients[client_name]
                    client.close()
                    break
                response = self.process_request(client_name, request)
                client.sendall(response.encode())
        except (ConnectionResetError, BrokenPipeError):
            print(f"Client {client_name} disconnected unexpectedly.")
            del self.clients[client_name]
            client.close()

    def process_request(self, client_name, request):
        request_data = json.loads(request)
        option = request_data.get('option')
        parameters = request_data.get('parameters', {})
        
        if option == "headlines":
            url = 'https://newsapi.org/v2/top-headlines'
        elif option == "sources":
            url = 'https://newsapi.org/v2/sources'
        else:
            return "Invalid option."

        params = {'apiKey': API_KEY, **parameters}
        response = requests.get(url, params=params)
        data = response.json()

        filename = f"{GROUP_ID}_{client_name}_{option}.json"
        with open(filename, 'w') as f:
            json.dump(data, f)

        if option == "headlines":
            results = [{'source': article['source']['name'], 'author': article['author'], 'title': article['title']} for article in data.get('articles', [])[:15]]
        elif option == "sources":
            results = [{'name': source['name'], 'country': source['country'], 'description': source['description'], 'url': source['url'], 'category': source['category'], 'language': source['language']} for source in data.get('sources', [])[:15]]
        
        return json.dumps(results)

if __name__ == "__main__":
    server = NewsServer()
    server.start_server()
