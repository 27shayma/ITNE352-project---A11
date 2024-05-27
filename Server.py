import socket
import requests
import json

# Indicates that the server is on
print ('=' * 5, 'Welcome to our server! Our server is on.', '=' * 5, '\n')

# Prompt the user to enter the API key
api_key = input("Please enter your NewsAPI.org API key: ")

# Prompt the user to enter the country code
country_code = input("Please enter the country code (2-letter ISO 3166-1 format): ")

# Set the API endpoint URL
url = f'https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={api_key}'

# Send a GET request to the API endpoint
response = requests.get(url)

# Check the status code of the response
if response.status_code != 200:
    print("Error! Failed to retrieve data. Status code:", response.status_code)
else:
    # Save the retrieved data to a JSON file
    with open("group_ID.json", "w") as file:
        json.dump(response.json(), file, indent=4)
    print("Retrieved data is added successfully!")
    print('-' * 15)

# Function Connect: Responsible for handling connections
def connect(client_socket, address, thread_no):
    print('\n', '+' * 5, 'Thread:', thread_no, 'is ready to receive the username from the client with address:',
          address, '+' * 5)
    # Exception Handling
    try:
        username = client_socket.recv(2048).decode('utf-8')  # Username is received
        if username == "User is terminating the connection":  # Terminated
            print('\nUnknown User (No username) terminated its connection')
            print('Currently connected clients are: ', clients)
            print('~' * 10)
        elif username == '':  # Empty username
            print(f"Thread {thread_no}: User did not enter a username. Closing connection.") 
            client_socket.close()  # socket connection is closed
            return
        else:
            print('\n', username, 'is connected to the server')
            clients.append(username)
            print('\nCurrently connected clients are: ', clients)
    except ConnectionResetError:
        print("Connection with address", address, "closed!")
        return
    # Handles the client's requests until they disconnect
    while True:
        counter = 0  # In order to count the number of headlines
        option = client_socket.recv(2048).decode('utf-8')
        try:
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
        # Opening the JSON file, in order to read the data
        with open('group_ID.json', 'r') as file:
            # Retrieving data
            data = json.load(file)
        # Client wants to retrieve top headlines
        if option == '1':
            info = []
            for article in data['articles']:
                counter += 1
                article_info = (
                    f"\n Headline:{counter}",
                    f"\n Title:{article['title']}",
                    f"\n Description:{article['description']}",
                    f"\n Author:{article['author']}",
                    f"\n Url:{article['url']}",
                    f"\n Publish Date:{article['publishedAt']}",
                    "\n" + "-" * 20
                )
                info.append(article_info)
            if not info:
                info = ['No headlines were found.']
            info = '\n'.join(' '.join(article_tuple) for article_tuple in info)
            client_socket.send(info.encode('utf-8'))
        # Client wants to retrieve sources
        elif option == '2':
            info = []
            for source in data['sources']:
                counter += 1
                source_info = (
                    f"\n Source:{counter}",
                    f"\n Name:{source['name']}",
                    f"\n Description:{source['description']}",
                    f"\n Url:{source['url']}",
                    f"\n Category:{source['category']}",
                    f"\n Language:{source['language']}",
                    "\n" + "-" * 20
                )
                info.append(source_info)
            if not info:
                info = ['No sources were found.']
            info = '\n'.join(' '.join(source_tuple) for source_tuple in info)
            client_socket.send(info.encode('utf-8'))

# Holds the connected clients
clients = []
# Counter for the threads
thread_count = 0
# Initialize a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Get the local machine name
ip = '127.0.0.2'
port = 55555
# Bind the socket to a specific address and port
server_socket.bind((ip, port))
# Listen for incoming connections
server_socket.listen()
while True:
    # Accept a new connection from a client
    client_socket, address = server_socket.accept()
    # Create a new thread for each client
    thread_count += 1
    t = threading.Thread(target=connect, args=(client_socket, address, thread_count))
    t.start()