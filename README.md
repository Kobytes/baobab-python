# BAOBAB - Best And Overpowered Beating Ass Brute-force 🚀

<p align="center">
  <img src="https://i.imgur.com/CIAo3RN.png" alt="BAOBAB Logo" width="500" height="500">
</p>

Welcome to BAOBAB version 1.1! 🎉 This release brings significant enhancements to my robust MySQL brute-forcing tool. BAOBAB uses the extensive [`rockyou.txt (not mandatory but highly recommended)`](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) wordlist, making it a prime choice for assessing password security on MySQL servers. Let’s dive into the latest improvements and features!

---

## 📢 Important Behavioral Update in Version 1.1

I'm excited to announce a significant behavioral change in BAOBAB with the introduction of Thread Modes in version 1.1! This update offers a more tailored brute-forcing experience by allowing users to choose from different operational modes, each utilizing a specific number of threads. This new feature enhances both performance and user control.

### Understanding Thread Modes 🧵

Thread Modes determine how many parallel threads are engaged during the brute-force process. While more threads can speed up the brute-forcing, it's crucial to understand their impact:

- **More threads can lead to faster results**, but they also consume more system resources.
- **Choosing the right mode** depends on your system capabilities and the urgency of the brute-force task.
- **Be cautious with resource-intensive modes** on systems with limited processing power to avoid system slowdowns.

### 📊 Thread Mode Breakdown

Here's a quick overview of each mode and its corresponding thread count:

| Mode          | Thread Count |
|---------------|--------------|
| Chill Mode    | 2 Threads    |
| Normal Mode   | 5 Threads    |
| Aggressive Mode | 10 Threads |

Choose the mode that best fits your needs and system capabilities. The Chill Mode is resource-friendly, Normal Mode balances speed and resource use, and Aggressive Mode harnesses maximum power for the quickest results.

---

## Features

- **Intuitive Interface**: Crafted with `customtkinter` for a sleek and easy-to-navigate experience.
- **Live Updates**: Real-time feedback with a comprehensive log and progress tracking. 📊
- **Password Complexity Analysis**: Classifies the complexity of uncovered passwords. 🔒
- **Error Tracking**: Maintains a detailed log file for error analysis and troubleshooting. 📝

## 📦 Installation

Ensure Python and the required libraries are installed on your system:

1. Clone or download the source code.
2. Install dependencies:

    ```bash
    pip install mysql-connector-python customtkinter
    ```

3. Launch the script:

    ```bash
    python baobab.py
    ```

## 🕹️ Usage

1. Run `baobab.py` to start.
2. Enter the MySQL host and user details.
3. Select or input the path to your `rockyou.txt` or any other wordlist.
4. Choose your bruteforce mode wisely between "Chill", "Normal" and "Aggressive".
5. Click "Start Brute-Force" to initiate.
7. Monitor progress in the log and progress bar.

## 💬 Contributing

Your contributions make BAOBAB better! Feature suggestions, bug reports, or code contributions are all welcome.

## ⚠️ Disclaimer

BAOBAB is for educational and ethical testing purposes only. I'm not liable for misuse or illegal activities. Always get explicit permission before testing any system.

---

aHR0cHM6Ly93d3cub3RlcmlhLmZyLw==

---

**Version 1.1 is a leap towards making BAOBAB more efficient, user-friendly, and robust. Enjoy the enhanced experience!** 🌟🚀
