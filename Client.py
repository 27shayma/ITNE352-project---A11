import socket
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import logging


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Client")
        self.root.geometry("600x400")

        self.client_socket = None

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.username_label = ttk.Label(self.main_frame, text="Enter your name:")
        self.username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self.main_frame)
        self.username_entry.pack(pady=10)

        self.connect_button = ttk.Button(self.main_frame, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=10)

        self.menu_frame = ttk.Frame(self.root)

        self.menu_label = ttk.Label(self.menu_frame, text="Main Menu")
        self.menu_label.pack(pady=10)

        self.headlines_button = ttk.Button(self.menu_frame, text="Search Headlines", command=self.show_headlines_menu)
        self.headlines_button.pack(pady=5)

        self.sources_button = ttk.Button(self.menu_frame, text="List of Sources", command=self.show_sources_menu)
        self.sources_button.pack(pady=5)

        self.quit_button = ttk.Button(self.menu_frame, text="Quit", command=self.quit_application)
        self.quit_button.pack(pady=5)

        self.headlines_frame = ttk.Frame(self.root)
        self.sources_frame = ttk.Frame(self.root)

        self.create_headlines_menu()
        self.create_sources_menu()

    def connect_to_server(self):
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Error", "Please enter your name")
            return
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 5555))
            self.client_socket.send(username.encode('utf-8'))
            self.main_frame.pack_forget()
            self.menu_frame.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
            logging.error(f"Failed to connect to server: {e}")

    def show_headlines_menu(self):
        self.menu_frame.pack_forget()
        self.headlines_frame.pack(fill="both", expand=True)

    def show_sources_menu(self):
        self.menu_frame.pack_forget()
        self.sources_frame.pack(fill="both", expand=True)

    def back_to_main_menu(self):
        self.headlines_frame.pack_forget()
        self.sources_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

    def create_headlines_menu(self):
        self.headlines_label = ttk.Label(self.headlines_frame, text="Headlines Menu")
        self.headlines_label.pack(pady=10)

        self.keyword_button = ttk.Button(self.headlines_frame, text="Search for Keywords", command=lambda: self.search_headlines('keyword'))
        self.keyword_button.pack(pady=5)

        self.category_button = ttk.Button(self.headlines_frame, text="Search by Category", command=lambda: self.search_headlines('category'))
        self.category_button.pack(pady=5)

        self.country_button = ttk.Button(self.headlines_frame, text="Search by Country", command=lambda: self.search_headlines('country'))
        self.country_button.pack(pady=5)

        self.all_headlines_button = ttk.Button(self.headlines_frame, text="List All New Headlines", command=lambda: self.search_headlines('all'))
        self.all_headlines_button.pack(pady=5)

        self.back_button = ttk.Button(self.headlines_frame, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_button.pack(pady=5)

        self.results_text = tk.Text(self.headlines_frame, wrap='word', height=15, width=70)
        self.results_text.pack(pady=10)

    def create_sources_menu(self):
        self.sources_label = ttk.Label(self.sources_frame, text="Sources Menu")
        self.sources_label.pack(pady=10)

        self.sources_category_button = ttk.Button(self.sources_frame, text="Search by Category", command=lambda: self.search_sources('category'))
        self.sources_category_button.pack(pady=5)

        self.sources_country_button = ttk.Button(self.sources_frame, text="Search by Country", command=lambda: self.search_sources('country'))
        self.sources_country_button.pack(pady=5)

        self.sources_language_button = ttk.Button(self.sources_frame, text="Search by Language", command=lambda: self.search_sources('language'))
        self.sources_language_button.pack(pady=5)

        self.all_sources_button = ttk.Button(self.sources_frame, text="List All Sources", command=lambda: self.search_sources('all'))
        self.all_sources_button.pack(pady=5)

        self.back_button = ttk.Button(self.sources_frame, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_button.pack(pady=5)

        self.results_text = tk.Text(self.sources_frame, wrap='word', height=15, width=70)
        self.results_text.pack(pady=10)

    def search_headlines(self, search_type):
        if search_type == 'keyword':
            keyword = simpledialog.askstring("Input", "Enter keyword:")
            request = f'headlines?q={keyword}'
        elif search_type == 'category':
            category = simpledialog.askstring("Input", "Enter category:")
            request = f'headlines?category={category}'
        elif search_type == 'country':
            country = simpledialog.askstring("Input", "Enter country:")
            request = f'headlines?country={country}'
        elif search_type == 'all':
            request = 'headlines?country=us'  # Default parameter to ensure a successful request
        else:
            return

        self.client_socket.send(request.encode('utf-8'))
        response = self.client_socket.recv(4096).decode('utf-8')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, json.loads(response)['data'])

    def search_sources(self, search_type):
        if search_type == 'category':
            category = simpledialog.askstring("Input", "Enter category:")
            request = f'sources?category={category}'
        elif search_type == 'country':
            country = simpledialog.askstring("Input", "Enter country:")
            request = f'sources?country={country}'
        elif search_type == 'language':
            language = simpledialog.askstring("Input", "Enter language:")
            request = f'sources?language={language}'
        elif search_type == 'all':
            request = 'sources?country=us'  # Default parameter to ensure a successful request
        else:
            return

        self.client_socket.send(request.encode('utf-8'))
        response = self.client_socket.recv(4096).decode('utf-8')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, json.loads(response)['data'])

    def back_to_main_menu(self):
        self.notebook.select(self.main_menu_frame)

    def main_menu(self):
        self.main_menu_button = ttk.Button(self.main_menu_frame, text="Back to Main Menu", command=self.main_menu)
        self.main_menu_button.pack(pady=10)

        self.headlines_button = ttk.Button(self.main_menu_frame, text="Headlines Menu", command=lambda: self.notebook.select(self.headlines_frame))
        self.headlines_button.pack(pady=5)

        self.sources_button = ttk.Button(self.main_menu_frame, text="Sources Menu", command=lambda: self.notebook.select(self.sources_frame))
        self.sources_button.pack(pady=5)

        self.quit_button = ttk.Button(self.main_menu_frame, text="Quit", command=self.destroy)
        self.quit_button.pack(pady=5)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("News Search")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    app = NewsSearchApp(root, client_socket)
    app.mainloop()
    client_socket.close()