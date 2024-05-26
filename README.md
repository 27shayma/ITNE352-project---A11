## The Project Title
# Multithreaded News Client/Server Information System

## Project Description
This project involves creating a client-server system to exchange current news information. The system will focus on key aspects of client-server architecture, network communication, multithreading, APIs, and coding best practices. The server, written in Python, retrieves news updates from NewsAPI.org, handles multiple client connections simultaneously, and responds to various client requests. The client script, also written in Python, connects to the server to fetch and display news and sources. Users can navigate through options to get specific news details or quit the application.

## Semester
S2 2023-2024

## Group
- Group Name:A11
- Course Code:ITNE352
- Section:1
- Students Name -ID: 
  1. Shaima Waleed Mohammed -202103160
  2. Ali Saeed Abdulmajeed-202209410

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
- **1-Python**: You need to ensure Python is installed on your system, if not please download it from their website [python.org]or go to this link (https://www.python.org/downloads/).
- **2-NewsAPI Key**: You need to Sign up on their website [NewsAPI.org](https://newsapi.org/) in order to get your API key.

### Setup
1. **Clone the repository**
2. **Create a virtual environment**
3. **Activate the virtual environment**

## How to Run the System
### First Start the Server file: `python server.py`
### Then Run the Client file: `python client.py `
After this, you need to write your name when prompted and through the menu options navigate to search for the news headlines or list sources.

## Project Scripts
### 1-Server Script (server.py)
The server script is designed to manage multiple client connections handle their requests for news information and retrieve news updates from NewsAPI.org.

#### Main Server Functionalities:
The server performs the following duties:
1-Startup and Connection Handling: The server initializes and waits for client connections. It can manage at least three simultaneous connections, displaying the client's name upon connection.
2-Request Handling: The server receives and processes client requests. It connects to NewsAPI.org to fetch relevant data, stores the data in a JSON file for testing, and sends a list of brief news details to the client.
3-Detail Retrieval: Upon client selection of a specific news item, the server sends detailed information about the chosen item.

#### Utilized Packages:


### 2-Client Script (client.py)
The client script is responsible for interacting with the server to request and display news information. Requests are sent to the server to display the results.

#### Main Client Functionalities:
The client performs the following tasks:
1-Connection Establishment: The client connects to the server, sending its username for identification.
2-Menu Display and Navigation: The client presents a main menu with various options. Users can navigate through the menus to request different types of news information, view lists of results, or return to previous menus.
3-Request Sending and Response Handling: The client sends requests based on user selections and displays the server's responses in an organized manner.

#### Utilized Packages:


## Additional Concepts
### M
-

## Acknowledgments
I would like to express my sincere gratitude to Dr. Mohammed Almeer for his invaluable guidance and support throughout this project. His insights and help were instrumental in the successful completion of this work. Additionally, I would like to thank NewsAPI for providing the news data used in this project. Their service was crucial in gathering the necessary information.

## Conclusion
This project built a multithreaded news client/server system using Python, effectively integrating NewsAPI.org for real-time news retrieval and distribution. It demonstrated key programming concepts like network communication, multithreading, and API.

## Resources
### Python : [python.org](https://www.python.org/downloads/).
### NewsAPI : [NewsAPI.org](https://newsapi.org/)
### Git : [https://git-scm.com/downloads)
