import uuid
import json

class User:
  def __init__(self, name, initial_balance=0):
    "Initialize a new user with a name, a unique registration code, and an initial balance."
    self.name = name
    self.registration_code = str(uuid.uuid4())[:8] # Unique registration code
    self.balance = initial_balance

  def add_balance(self, amount):
    "Add Ritcoins to the user's balance"
    if amount > 0:
      self.balance += amount
      return True
    return False
  
  def subtract_balance(self, amount):
    "Substract Ritcoins from the user's balance if enough balance exists."
    if 0 < amount <= self.balance:
      self.balance -= amount
      return True
    return False
  
  def get_info(self):
    "Return user details as a dictionary."
    return {
      "name": self.name,
      "registration_code": self.registration_code,
      "balance": self.balance
    }
  
class Bank:
  def __init__(self):
    "Initialize a new bank with an empty list of users."
    self.users = {}
  
  def add_user(self, name, initial_balance=0):
    "Add a new user to the bank."
    new_user = User(name, initial_balance)
    self.users[new_user.registration_code] = new_user
    return new_user.registration_code # Return the unique registration code
  
  def find_user(self, registration_code):
    "Find a user by their registration code."
    return self.users.get(registration_code)
  
  def list_users(self):
    "List all users in the bank."
    return [user.get_info() for user in self.users.values()]
  
  def save_to_file(self, filename='users.json'):
    "Save all user data to a JSON file."
    with open(filename, "w") as file:
      # Convert dictionary of users into a JSON-serializable format
      json.dump(
        {reg_code: user.get_info() for reg_code, user in self.users.items()},
        file,
        indent=4
      )
    print(f"Data saved to {filename}.")

  def load_from_file(self, filename="users.json"):
    "Load user data from a JSON file."
    try:
      with open(filename, "r") as file:
        data = json.load(file)
        for reg_code, user_data in data.items():
          user = User(user_data["name"], user_data["balance"])
          user.registration_code = reg_code  # Restore the original registration code
          self.users[reg_code] = user
      print(f"Data loaded from {filename}.")
    except FileNotFoundError:
      print(f"No file named {filename} found. Starting with an empty bank.")
  

def main():
  bank = Bank()

  # Load data at the start
  bank.load_from_file()

  while True:
    print("\n-- Bank Menu ---")
    print("1. Create a new user")
    print("2. Add balance to a user")
    print("3. Substract balance from a user")
    print("4. Display all users")
    print("5. Exit")

    choice = input("choose an option: ").strip()

    if choice == "1":
      # Create a new user
      name = input("Enter the user's name: ").strip()
      balance = input("Enter the initial balance (default 0): ").strip()
      initial_balance = int(balance) if balance.isdigit() else 0
      reg_code = bank.add_user(name, initial_balance)
      print(f"User created. Registration code: {reg_code}")

    elif(choice == "2"):
      # Add balance
      reg_code = input("Enter the user's registration code: ").strip()
      user = bank.find_user(reg_code)
      if user:
        amount = int(input("Enter the amount to add: ").strip())
        if user.add_balance(amount):
          print(f"Added {amount} Ritcoins. New balance: {user.balance}")
        else:
          print("Invalid amount.")
      else:
        print("User not found!")
    
    elif(choice == "3"):
      # Subtract balance
      reg_code = input("Enter the user's registration code: ").strip()
      user = bank.find_user(reg_code)
      if user:
        amount = int(input("Enter the amount to subtract: ").strip())
        if user.subtract_balance(amount):
          print(f"Subtracted {amount} Ritcoins. New balance: {user.balance}")
        else:
          print("invalid amount ou insufficient balance.")
      else:
        print("User not found!")

    elif(choice == "4"):
      # Display all users
      users = bank.list_users()
      if users:
        print("\n--- List of Users ---")
        for user_info in users:
          print(f"name: {user_info['name']}, Code: {user_info['registration_code']}, Balance: {user_info['balance']}")
      else:
        print("No users found!")

    elif choice == "5":
        # Save data before exiting
        bank.save_to_file()
        print("Exiting program. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
    

if __name__ == "__main__":
  main()