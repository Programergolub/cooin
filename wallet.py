import json
import time
import random
import os
import string
import tkinter as tk
from tkinter import messagebox

DATA_FILE = 'cooin_data.json'
# Wallet settings (used for display, not mining)
MINE_COST = 0.005

# --- Utility Functions (Shared with Miner) ---

def generate_wallet_address():
    """Generates a random 16-character alphanumeric wallet address (Token)."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=16))

def load_all_wallets():
    """Loads all wallets from the JSON file. Initializes the 'wallets' map if file is new."""
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
        # In a GUI app, we silence warnings but return a safe default
        return default_data

def save_all_wallets(data):
    """Saves the entire wallet data dictionary to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        messagebox.showerror("File Error", "Could not save wallet data. Check file permissions.")

# --- Main Application Class ---

class CooinWalletApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🕊️ Cooin Roost Chain Wallet (v2.0)")
        self.geometry("400x450")
        self.resizable(False, False)
        
        # State variables
        self.current_address = None
        self.all_wallets = load_all_wallets()

        # Container for stacking frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.create_frames()
        self.show_frame(AuthFrame)

    def create_frames(self):
        """Initializes all pages/frames."""
        for F in (AuthFrame, WalletFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        """Raises the selected frame to the top."""
        frame = self.frames[cont]
        frame.tkraise()

    def login_success(self, address):
        """Called upon successful login or registration."""
        self.current_address = address
        wallet_frame = self.frames[WalletFrame]
        wallet_frame.update_status() # Load and display current wallet data
        self.show_frame(WalletFrame)

    def logout(self):
        """Clears the session and returns to the authentication screen."""
        self.current_address = None
        self.show_frame(AuthFrame)

# --- Authentication Frame ---

class AuthFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="Cooin Authentication", font=('Arial', 16, 'bold')).pack(pady=10)
        tk.Label(self, text="16-Character Wallet Address (Token):").pack(pady=5)
        
        self.address_entry = tk.Entry(self, width=30, font=('Courier', 10))
        self.address_entry.pack(pady=5, padx=20)
        
        tk.Button(self, text="Login to Existing Wallet", command=self.login, 
                  bg='#00BFFF', fg='white', font=('Arial', 10, 'bold')).pack(pady=10, ipadx=10)
        
        tk.Button(self, text="Register New Wallet", command=self.register, 
                  bg='#3CB371', fg='white', font=('Arial', 10, 'bold')).pack(pady=10, ipadx=10)

    def login(self):
        address = self.address_entry.get().strip()
        self.controller.all_wallets = load_all_wallets() # Refresh wallets before login
        
        if address in self.controller.all_wallets['wallets']:
            messagebox.showinfo("Success", f"Logged in as {address[:8]}...")
            self.controller.login_success(address)
        else:
            messagebox.showerror("Login Failed", "Address not found in the Roost Chain ledger.")
            
    def register(self):
        self.controller.all_wallets = load_all_wallets()
        
        new_address = generate_wallet_address()
        
        # Initialize new wallet data
        self.controller.all_wallets['wallets'][new_address] = {
            "balance": 0.0,
            "flight_score": 1.0, 
            "wallet_address": new_address
        }
        
        save_all_wallets(self.controller.all_wallets)
        
        messagebox.showinfo("Registration Success", 
                            f"New Wallet Created!\nYour Address: {new_address}\n\n"
                            "This is your permanent login token. Write it down!")
        
        self.controller.login_success(new_address)
        self.address_entry.delete(0, tk.END) # Clear field after successful register

# --- Wallet Status Frame ---

class WalletFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="🕊️ Active Cooin Wallet Status", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Address Display
        tk.Label(self, text="Wallet Address:", font=('Arial', 10, 'underline')).pack()
        self.address_label = tk.Label(self, text="N/A", font=('Courier', 11), fg='#333333', wraplength=350)
        self.address_label.pack(pady=5)
        
        # Balance Display
        tk.Label(self, text="Current Balance:", font=('Arial', 10, 'underline')).pack()
        self.balance_label = tk.Label(self, text="0.0000 COO", font=('Arial', 24, 'bold'), fg='#3CB371')
        self.balance_label.pack(pady=10)
        
        # Flight Score Display
        tk.Label(self, text="Flight Score (PoF Efficiency):", font=('Arial', 10, 'underline')).pack()
        self.score_label = tk.Label(self, text="1.00", font=('Arial', 14))
        self.score_label.pack(pady=5)

        # Mining Hint
        tk.Label(self, text=f"(Mining Cost: {MINE_COST:.4f} COO)", font=('Arial', 8)).pack(pady=5)

        # Action Buttons
        tk.Button(self, text="Refresh Status", command=self.update_status, 
                  bg='#F0E68C', fg='black', font=('Arial', 10)).pack(pady=10, ipadx=20)
        
        tk.Button(self, text="Logout", command=self.controller.logout, 
                  bg='#FF4500', fg='white', font=('Arial', 10, 'bold')).pack(pady=20, ipadx=30)
        
        tk.Label(self, text="*Run cooin_miner.py or cooin_earner_app.py to change balance*", 
                 font=('Arial', 8, 'italic')).pack(pady=5)


    def update_status(self):
        """Fetches the latest data from the JSON file and updates GUI labels."""
        if not self.controller.current_address:
            return

        # Reload all wallets to get the latest data from the ledger
        self.controller.all_wallets = load_all_wallets()
        current_address = self.controller.current_address
        
        # Check if the address exists after reload
        if current_address in self.controller.all_wallets['wallets']:
            wallet_data = self.controller.all_wallets['wallets'][current_address]
            
            self.address_label.config(text=wallet_data['wallet_address'])
            self.balance_label.config(text=f"{wallet_data['balance']:.4f} COO")
            self.score_label.config(text=f"{wallet_data['flight_score']:.2f}")
            self.controller.title(f"🕊️ Cooin Wallet - {current_address[:8]}...")
            
        else:
            # Should not happen under normal operation, but handles ledger corruption
            messagebox.showerror("Error", "Wallet data missing. Logging out.")
            self.controller.logout()


if __name__ == "__main__":
    app = CooinWalletApp()
    app.mainloop()
