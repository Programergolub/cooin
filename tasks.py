import json
import time
import random
import os
import string
import tkinter as tk
from tkinter import messagebox

DATA_FILE = 'cooin_data.json'
DAILY_TASK_REWARD = 0.5 # Fixed, guaranteed reward for a quick task

# --- Utility Functions (Shared) ---

def load_all_wallets():
    """Loads all wallets from the JSON file."""
    default_data = {"wallets": {}}

    if not os.path.exists(DATA_FILE):
        return default_data
    
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            if 'wallets' not in data:
                return default_data
            return data
            
    except (json.JSONDecodeError, IOError):
        # In GUI, show a message box instead of printing
        messagebox.showerror("File Error", "Ledger file corrupted or empty. Please register a wallet first.")
        return default_data

def save_all_wallets(data):
    """Saves the entire wallet data dictionary to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        messagebox.showerror("Save Error", f"Error saving data file: {e}")

# --- GUI Application Class ---

class TaskApp:
    def __init__(self, master):
        self.master = master
        master.title("Cooin Daily Task Client 🐦")
        master.geometry("400x350")
        master.configure(bg='#f0f0f0')

        self.current_address = None
        self.wallet_data = None

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.login_screen()

    # --- Task Logic ---
    def complete_daily_task(self):
        """Simulates a quick, daily pigeon task to earn a guaranteed reward."""
        if not self.current_address:
            messagebox.showerror("Error", "Please log in first.")
            return

        all_wallets = load_all_wallets()
        
        # Ensure we are operating on the latest data
        if self.current_address not in all_wallets['wallets']:
            messagebox.showerror("Error", "Wallet not found. Please log in again.")
            self.login_screen()
            return
            
        self.wallet_data = all_wallets['wallets'][self.current_address]
        
        tasks = [
            "Scouting the high-rise for fresh seeds",
            "Delivering a non-urgent message (local)",
            "Performing a routine maintenance peck on the Roost node",
            "Gathering materials for a community nest"
        ]
        
        task_name = random.choice(tasks)
        
        # Simulate work visually (simple dialog for simulation)
        messagebox.showinfo("Task In Progress", f"🐦 Initiating Daily Task: {task_name}...")
        
        # Grant reward
        reward = DAILY_TASK_REWARD
        self.wallet_data['balance'] += reward
        
        # Save and update the display
        all_wallets['wallets'][self.current_address] = self.wallet_data
        save_all_wallets(all_wallets)
        
        messagebox.showinfo("Success!", f"🎉 TASK COMPLETE! You earned {reward:.4f} COO.")
        self.update_status_display()
        
    def update_status_display(self):
        """Refreshes the balance and address labels."""
        all_wallets = load_all_wallets()
        if self.current_address in all_wallets['wallets']:
            self.wallet_data = all_wallets['wallets'][self.current_address]
            self.address_label.config(text=f"Address: {self.current_address}", fg='#006400')
            self.balance_label.config(text=f"Balance: {self.wallet_data['balance']:.4f} COO", fg='#8B4513')
        else:
            self.address_label.config(text="Address: LOGGED OUT", fg='red')
            self.balance_label.config(text="Balance: 0.0000 COO", fg='red')

    # --- GUI Screens and Transitions ---

    def clear_frame(self):
        """Destroys all widgets in the master window."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def login_screen(self):
        """Displays the login screen for the wallet address."""
        self.clear_frame()
        
        # Main Frame setup
        login_frame = tk.Frame(self.master, padx=20, pady=20, bg='#f0f0f0')
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(login_frame, text="Cooin Task Client Login", font=("Arial", 16, "bold"), bg='#f0f0f0', fg='#333333').pack(pady=10)

        # Address Input
        tk.Label(login_frame, text="16-Char Wallet Address:", bg='#f0f0f0', fg='#555555').pack(pady=(10, 0))
        self.address_entry = tk.Entry(login_frame, width=30, bd=2, relief=tk.FLAT)
        self.address_entry.pack(ipady=5, pady=5)
        
        # Login Button
        login_button = tk.Button(login_frame, text="Login & Start Tasking", command=self.attempt_login, bg='#4CAF50', fg='white', font=("Arial", 12, "bold"), relief=tk.FLAT, activebackground='#45a049')
        login_button.pack(pady=20, ipadx=10, ipady=5)
        
        tk.Label(login_frame, text="Use 'cooin_wallet.py' to register new addresses.", font=("Arial", 9, "italic"), bg='#f0f0f0', fg='#777777').pack(pady=5)
        
    def attempt_login(self):
        """Checks if the entered address is valid and transitions to the task screen."""
        address = self.address_entry.get().strip()
        all_wallets = load_all_wallets()
        
        if address in all_wallets['wallets']:
            self.current_address = address
            self.wallet_data = all_wallets['wallets'][address]
            self.task_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid or unregistered 16-character address.")

    def task_screen(self):
        """Displays the main task execution screen."""
        self.clear_frame()
        
        # Main Task Frame
        task_frame = tk.Frame(self.master, padx=20, pady=20, bg='#FFFFFF', relief=tk.GROOVE, bd=1)
        task_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(task_frame, text="Pigeon Daily Task Hub", font=("Arial", 16, "bold"), bg='#FFFFFF', fg='#333333').pack(pady=10)

        # Address Display
        self.address_label = tk.Label(task_frame, text="", font=("Arial", 10), bg='#FFFFFF')
        self.address_label.pack(pady=5)
        
        # Balance Display
        self.balance_label = tk.Label(task_frame, text="", font=("Arial", 14, "bold"), bg='#FFFFFF')
        self.balance_label.pack(pady=10)
        
        # Task Button
        task_button = tk.Button(task_frame, text="COMPLETE DAILY TASK (0.5 COO)", command=self.complete_daily_task, 
                                bg='#FFC107', fg='#333333', font=("Arial", 12, "bold"), relief=tk.FLAT, activebackground='#ffaa00')
        task_button.pack(pady=20, ipadx=10, ipady=10)

        # Logout Button
        logout_button = tk.Button(task_frame, text="Logout", command=self.logout, bg='#d9534f', fg='white', relief=tk.FLAT, activebackground='#c9302c')
        logout_button.pack(pady=10)

        self.update_status_display()

    def logout(self):
        """Clears the session and returns to the login screen."""
        self.current_address = None
        self.wallet_data = None
        self.login_screen()


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
