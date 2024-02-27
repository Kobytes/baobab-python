# BAOBAB - Best And Overpowered Beating Ass Brute-force

BAOBAB is a powerful and user-friendly GUI tool for brute-forcing MySQL passwords. It leverages the extensive [`rockyou.txt`](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) wordlist to attempt access into MySQL databases, making it an ideal tool for testing password strength and security in MySQL servers. This latest update brings significant improvements in performance, efficiency, and user experience.

## New Features and Enhancements

- Object-Oriented Programming Refactor:
    - Introduction of BruteForceSQL class for better code organization and maintainability.
    - Enhanced readability and structure through OOP practices.

- Improved User Interface:
    - Creation of BruteForceGUI class for a clear separation between UI logic and business logic.
    - Redesigned user interface for a more intuitive and user-friendly experience.

- Brute-Force Process Interruption Feature:
    - Ability to stop the ongoing brute-force process, offering more control and flexibility to the users.
    - Performance and Security Optimizations:

- Improved thread management for enhanced performance.
- Strengthened exception handling and logging for increased reliability.

## Features

- **User-Friendly Interface**: Built with `customtkinter` for a modern and easy-to-use interface.
- **Real-Time Feedback**: Provides live updates on the brute-forcing process with a detailed log and progress bar.
- **Complexity Analysis**: Classifies found passwords based on their complexity (low, medium, high).
- **Error Logging**: Records errors into a log file for troubleshooting and analysis.

## Installation

To use BAOBAB, ensure you have Python installed on your system along with the necessary libraries. 

1. Clone this repository or download the source code.
2. Install required Python packages:

    ```bash
    pip install mysql-connector-python customtkinter
    ```

3. Run the script:

    ```bash
    python baobab.py
    ```

## Usage

1. Start the application by running `baobab.py`.
2. Enter the target MySQL host and user credentials.
3. Choose or enter the path to your `rockyou.txt` wordlist.
4. Click "Start Brute-Force" to begin the brute-forcing process.
5. Monitor the progress in the real-time log and progress bar.

## Contributing

Contributions to BAOBAB are welcome! Whether it's feature requests, bug reports, or code contributions, please feel free to make your suggestions known.

## Disclaimer

BAOBAB is developed for educational and ethical testing purposes only. The authors are not responsible for any misuse or illegal activities. Always obtain explicit permission before testing any system.

---

aHR0cHM6Ly93d3cub3RlcmlhLmZyLw==
