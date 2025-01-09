from flask import Flask, jsonify, request, render_template
import uuid
import json
from wallet import generate_three_digit_id

app = Flask(__name__)

# Load existing users from the JSON file
def load_users(filename="users.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save users to the JSON file
def save_users(users, filename="users.json"):
    with open(filename, "w") as file:
        json.dump(users, file, indent=4)

# Initialize users
users = load_users()

# Route: Home page
@app.route("/")
def home():
    return render_template("index.html")

# Route: Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

# Route: Add a new user
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")
    balance = data.get("balance", 0)
    
    # Generate a new user
    reg_code = str(uuid.uuid4())[:8]
    users[reg_code] = {
        "name": name,
        "registration_code": reg_code,
        "balance": balance
    }
    save_users(users)  # Save to the JSON file
    return jsonify({"message": "User added!", "registration_code": reg_code}), 201

# Route: Update user balance
@app.route("/update_balance/<reg_code>", methods=["PUT"])
def update_balance(reg_code):
    data = request.json
    amount = data.get("amount")
    user = users.get(reg_code)
    print(f"Received reg_code: {reg_code}")
    print(f"Available keys in users: {list(users.keys())}")
    
    if user:
        user["balance"] += amount
        save_users(users)  # Save the updated users
        return jsonify({"message": "Balance updated!", "new_balance": user["balance"]}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Route: Delete a user
@app.route("/delete_user/<reg_code>", methods=["DELETE"])
def delete_user(reg_code):
    if reg_code in users:
        del users[reg_code]
        save_users(users)  # Save the updated users
        return jsonify({"message": "User deleted!"}), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
# Load wallets from wallets.json
def load_wallets(filename="wallets.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    
# Dynamic route for user wallets
@app.route("/wallet/<username>-<user_id>")
def user_wallet(username, user_id):
    wallets = load_wallets()
    matching_user = None

    for reg_code, user_wallet in wallets.items():
        if user_wallet["name"].lower() == username.lower():
            expected_id = generate_three_digit_id(reg_code)
            if expected_id == user_id:
                matching_user = user_wallet
                break
    if not matching_user:
        return "User not found", 404
    
    # Render the wallet.html with user-specific data
    return render_template("wallet.html", user=matching_user)


if __name__ == "__main__":
    app.run(debug=True)
