import json
import zlib

def generate_crc32_hash(reg_code):
  "Generate a CRC32 hash from the given registration code"
  crc_hash = zlib.crc32(reg_code.encode('utf-8'))
  return f"{crc_hash:08x}" # Convert to an 8-character hexadecimal string

def generate_three_digit_id(reg_code):
  "Generate a unique three-digit ID for a user based on their registration code."
  crc_id = zlib.crc32(reg_code.encode('utf-8'))
  return f"{crc_id % 1000:03}"  # Ensure 3 digits

def load_users(filename='users.json'):
  "Load user data from the JSON file"
  try:
    with open(filename, "r") as file:
      return json.load(file)
  except FileNotFoundError:
    print(f"Error: {filename} not found.")
    return {}
  
def generate_wallets(users):
  "Generate wallets for all users."
  wallets = {}
  for reg_code, user_data in users.items():
    address = generate_crc32_hash(reg_code) # generate the wallet address
    crc_id = generate_three_digit_id(reg_code) # generate the id user
    wallets[reg_code] = {
      "name": user_data["name"],
      "id": crc_id,
      "registration_code": reg_code,
      "balance": user_data["balance"],
      "address": address # add the wallet address
    }
  return wallets

def save_wallets(wallets, filename="wallets.json"):
  "Save the wallets to a new JSON file."
  with open(filename, "w") as file:
    json.dump(wallets, file, indent=4)
  print(f"Wallets saved to {filename}.")



if __name__ == "__main__":
  # Load user data
  users = load_users("users.json")

  # Generate wallets
  wallets = generate_wallets(users)

  # Save wallets to a new file
  save_wallets(wallets)
