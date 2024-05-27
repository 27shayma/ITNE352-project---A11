import socket
import requests
import json
import threading

print('=' * 5, 'Welcome to our server! Our server is on.', '=' * 5, '\n')

api_key = input("Please enter your NewsAPI.org API key: ")
country_code = input("Please enter the country code (2-letter ISO 3166-1 format): ")

url = f'https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={api_key}'

response = requests.get(url)

if response.status_code != 200:
    print("Error! Failed to retrieve data. Status code:", response.status_code)
else:
    with open("group_ID.json", "w") as file:
        json.dump(response.json(), file, indent=4)
    print("Retrieved data is added successfully!")
    print('-' * 15)

def connect(client_socket, address, thread_no):
    print('\n', '+' * 5, 'Thread:', thread_no, 'is ready to receive the username from the client with address:',
          address, '+' * 5)
    try:
        username = client_socket.recv(2048).decode('utf-8')
        if username == "User is terminating the connection":
            print('\nUnknown User (No username) terminated its connection')
            print('Currently connected clients are: ', clients)
            print('~' * 10)
        elif username == '':
            print(f"Thread {thread_no}: User did not enter a username. Closing connection.")
            client_socket.close()
            return
        else:
            print('\n', username, 'is connected to the server')
            clients.append(username)
            print('\nCurrently connected clients are: ', clients)
    except ConnectionResetError:
        print("Connection with address", address, "closed!")
        return

    while True:
        counter = 0
        try:
            option = client_socket.recv(2048).decode('utf-8')
            if option == '1':
                print(username, 'chose the option number', option, ": Top Headlines")
            elif option == '2':
                print(username, 'chose the option number', option, ": Sources")
            else:
                print('\n', username, ' is disconnected')
                clients.remove(username)
                print('~' * 10)
                client_socket.close()
                return
        except ConnectionResetError:
            print('\n', username, ' connection was reset by the server.')
            clients.remove(username)
            client_socket.close()
            return

        with open('group_ID.json', 'r') as file:
            data = json.load(file)

        if option == '1':
            info = []
            for article in data['articles']:
                counter += 1
                article_info = (
                    f"\n Headline: {counter}",
                    f"\n Title: {article['title']}",
                    f"\n Description: {article['description']}",
                    f"\n Author: {article['author']}",
                    f"\n Url: {article['url']}",
                    f"\n Publish Date: {article['publishedAt']}",
                    "\n" + "-" * 20
                )
                info.append(article_info)
            if not info:
                info = ['No headlines were found.']
            info = '\n'.join(' '.join(article_tuple) for article_tuple in info)
            try:
                client_socket.send(info.encode('utf-8'))
            except ConnectionResetError:
                print("Failed to send data. Connection reset by client.")
                clients.remove(username)
                client_socket.close()
                return

        elif option == '2':
            info = []
            url_sources = f'https://newsapi.org/v2/sources?apiKey={api_key}'
            response_sources = requests.get(url_sources)
            if response_sources.status_code == 200:
                data_sources = response_sources.json()
                for source in data_sources['sources']:
                    counter += 1
                    source_info = (
                        f"\n Source: {counter}",
                        f"\n Name: {source['name']}",
                        f"\n Description: {source['description']}",
                        f"\n Url: {source['url']}",
                        f"\n Category: {source['category']}",
                        f"\n Language: {source['language']}",
                        "\n" + "-" * 20
                    )
                    info.append(source_info)
            if not info:
                info = ['No sources were found.']
            info = '\n'.join(' '.join(source_tuple) for source_tuple in info)
            try:
                client_socket.send(info.encode('utf-8'))
            except ConnectionResetError:
                print("Failed to send data. Connection reset by client.")
                clients.remove(username)
                client_socket.close()
                return

clients = []
thread_count = 0
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 12345
server_socket.bind((ip, port))
server_socket.listen()
print(f"Server is listening on {ip}:{port}")
while True:
    client_socket, address = server_socket.accept()
    thread_count += 1
    t = threading.Thread(target=connect, args=(client_socket, address, thread_count))
    t.start()