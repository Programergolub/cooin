import json
import time
import random
import os
import string

DATA_FILE = 'cooin_data.json'
# Rewards and difficulty settings (Miner-specific)
BASE_MINE_REWARD = 1.0 
MINE_COST = 0.005
FLIGHT_SCORE_INCREASE = 0.01

# --- Utility Functions (Shared with Wallet) ---

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
        print("Warning: Ledger file corrupted or empty. Cannot mine until a wallet exists.")
        return default_data

def save_all_wallets(data):
    """Saves the entire wallet data dictionary to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data file: {e}")

# --- Mining Logic ---

def display_miner_status(wallet_data):
    """Displays essential mining stats for the logged-in user."""
    print("\n" + "="*50)
    print(f"⛏️  Cooin PoF Mining Client - Active Session")
    print("="*50)
    print(f"Target Wallet: {wallet_data['wallet_address']}")
    print(f"Current Balance: {wallet_data['balance']:.4f} COO")
    print(f"Flight Score (Efficiency): {wallet_data['flight_score']:.2f}")
    print(f"Cost per PoF Flight: {MINE_COST:.4f} COO")
    print("="*50 + "\n")

def view_history(all_wallets, current_address):
    """Displays the last 5 Flight Score entries for the user."""
    wallet_data = all_wallets['wallets'][current_address]
    
    # Initialize history list if it's missing (e.g., wallet created before this feature)
    if 'flight_score_history' not in wallet_data or not isinstance(wallet_data['flight_score_history'], list):
        wallet_data['flight_score_history'] = [wallet_data.get('flight_score', 1.0)]
        save_all_wallets(all_wallets)
        
    history = wallet_data['flight_score_history']
    
    print("\n--- Flight Score History (Last 5 Updates) ---")
    if len(history) <= 1:
        print("No significant mining history yet. Start flying!")
        print("------------------------------------------")
        time.sleep(1)
        return
        
    
    # Display the last few entries
    display_list = history[-5:]
    
    for i, score in enumerate(display_list):
        if i == len(display_list) - 1:
            print(f"[{len(history) - len(display_list) + i + 1}] Current Score: {score:.4f} (LATEST)")
        else:
            print(f"[{len(history) - len(display_list) + i + 1}] Score: {score:.4f}")
    
    print("------------------------------------------")
    time.sleep(2)


def simulate_mining(all_wallets, current_address):
    """Simulates Proof-of-Flight (PoF) consensus mining for the current user."""
    wallet_data = all_wallets['wallets'][current_address]
    
    if wallet_data['balance'] < MINE_COST:
        print(f"❌ ERROR: Not enough Cooin to initiate flight. Need {MINE_COST:.4f} COO.")
        print("Suggestion: Use the 'cooin_task_app.py' to earn your initial balance!")
        time.sleep(2)
        return

    # Deduct the cost immediately (this is the cost of the "postage")
    wallet_data['balance'] -= MINE_COST
    # Note: History tracking needs to be initialized if not present
    if 'flight_score_history' not in wallet_data or not isinstance(wallet_data['flight_score_history'], list):
        wallet_data['flight_score_history'] = [wallet_data.get('flight_score', 1.0)]

    save_all_wallets(all_wallets)
    
    print("🚀 Initiating Proof-of-Flight... The Cooin Carrier Pigeon is airborne!")
    
    # Mining duration simulation
    delay_time = 3 + random.random() * 2 # 3 to 5 second wait
    
    # Visual loading bar
    for i in range(1, 11):
        print(f"|{'#' * i}{'.' * (10 - i)}| Verifying delivery... ({i*10}%)", end='\r')
        time.sleep(delay_time / 10)
    print("\n") 

    # Success chance increases with Flight Score (up to a max of 95%)
    base_success_chance = 0.6 
    success_chance = min(0.95, base_success_chance + (wallet_data['flight_score'] - 1.0) / 10)

    if random.random() < success_chance:
        reward = BASE_MINE_REWARD * random.uniform(0.9, 1.1)
        
        # Update balance and flight score on successful "delivery"
        wallet_data['balance'] += reward
        wallet_data['flight_score'] += FLIGHT_SCORE_INCREASE
        
        # Track history
        wallet_data['flight_score_history'].append(wallet_data['flight_score'])
        
        save_all_wallets(all_wallets)
        print(f"✅ SUCCESS! Block confirmed by Cooin. You earned {reward:.4f} COO.")
        print(f"      -> Flight Score increased to {wallet_data['flight_score']:.2f}!")
    else:
        print("⚠️ FAILURE: Carrier pigeon encountered turbulence. No block found this time.")
        print(f"      -> Flight Score remains {wallet_data['flight_score']:.2f}. Try again!")
        
    time.sleep(1) 

# --- Main Execution ---

def main():
    print("\n--- Cooin Proof-of-Flight Miner Client ---")
    current_address = None
    
    while not current_address:
        all_wallets = load_all_wallets()
        
        if not all_wallets or not all_wallets.get('wallets'):
            print("\n❌ No Cooin Wallets found. Please register one first using 'cooin_wallet.py'.")
            time.sleep(2)
            return

        print("\n--- Miner Login ---")
        address_input = input("Enter your 16-character Wallet Address (Miner Target): ").strip()
        
        if address_input in all_wallets['wallets']:
            current_address = address_input
            print(f"\n✅ Miner Logged in. Ready to mine for: {current_address}")
            time.sleep(1)
        else:
            print("\n❌ Invalid Address. Cannot start mining session.")
            time.sleep(1)

    # Mining Session Loop
    while current_address:
        all_wallets = load_all_wallets()
        wallet_data = all_wallets['wallets'][current_address]
        
        display_miner_status(wallet_data)
        
        print("1. Start PoF Mining (Generate Cooin)")
        print("2. View Flight Score History")
        print("3. Logout and Close Miner")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            simulate_mining(all_wallets, current_address)
        elif choice == '2':
            view_history(all_wallets, current_address)
        elif choice == '3':
            print(f"Logging out of mining session for {current_address}.")
            current_address = None # End loop
            time.sleep(1)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            time.sleep(1)

if __name__ == "__main__":
    main()
