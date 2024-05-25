## Project Title
# News Aggregator and Distribution Server

## Project Description
This project involves creating a client-server system to exchange current news information. The system will focus on key aspects of client-server architecture, network communication, multithreading, APIs, and coding best practices. The server, written in Python, retrieves news updates from NewsAPI.org, handles multiple client connections simultaneously, and responds to various client requests. The client script, also written in Python, connects to the server to fetch and display news and sources. Users can navigate through options to get specific news details or quit the application.

## Semester
S2 2023-2024

## Group
- Group Name:A11
- Course Code:ITNE352
- Section:1
- Students Name: 
  1. Shaima Waleed Mohammed 
  2. 
- Student ID:
  1. 202103160
  2. 2021

## Table of Contents
1. [Requirements](#Requirements)
2. [How to Run](#How-to-Run)
3. [The Scripts](#The-Scripts)
4. [Additional Concepts](#Additional-Concepts)
5. [Acknowledgments](#Acknowledgments)
6. [Conclusion](#Conclusion)
7. [Resources](#Resources)

## Requirements
To set up and ensure an efficient run of this project on your local machine, follow these instructions:

### Prerequisites
- **1-Python**: Ensure Python is installed on your system , if not please download it from their website [python.org]or go to this link (https://www.python.org/downloads/).
- **2-NewsAPI Key**: You need to Sign up on their website [NewsAPI.org](https://newsapi.org/) in order to get your API key.

### Setup
1. **Clone the repository**
2. **Create a virtual environment**
3. **Activate the virtual environment**

## How to Run the System
### First Start the Server : `python server.py`
### Then Run the Client : `python client.py `
After this you need to write your name when prompted and through the menu options navigate to search for the news headlines or list sources.

## Project Scripts
### 1-Server Script (server.py)
The server script retrieves news updates from NewsAPI.org and manages multiple client connections using multithreading. It handles different types of requests and sends the appropriate responses to the clients.

#### Main Functionalities:
Fetching news from NewsAPI based on different endpoints and parameters.
Handling multiple simultaneous client connections.
Sending JSON responses to clients.
Logging client connections and requests.

#### Utilized Packages:
socket for network communication.
threading for handling multiple clients.
requests for fetching news from NewsAPI.
json for processing JSON data.

### 2-Client Script (client.py)
The client script presents a menu system to the user, allowing them to search for news headlines or list sources. It sends requests to the server and displays the results.

#### Main Functionalities:
Sending requests to the server based on user input.
Displaying news headlines and sources.
Navigating through a hierarchical menu system.

#### Utilized Packages:
socket for network communication.
json for processing JSON data.

## Additional Concepts
### Multithreading
The server uses multithreading to handle multiple clients simultaneously. This allows the server to manage several connections at once without blocking.

## Acknowledgments
Special thanks to our professor Dr. Mohammed Almeer for providing guidance and resources for this project.
Thanks to NewsAPI for providing the news data used in this project.

## Conclusion
This project demonstrates the implementation of a client-server architecture for retrieving and displaying news data. It highlights the use of network communication, multithreading, and API integration in Python.

## Resources
### Python Documentation : [python.org](https://www.python.org/downloads/).
### NewsAPI Documentation : [NewsAPI.org](https://newsapi.org/)
