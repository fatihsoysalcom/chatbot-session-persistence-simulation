import json
import os

# In a real application, this would be a database or a more robust storage mechanism.
# For this example, we'll simulate persistence using a simple JSON file.
PERSISTENCE_FILE = 'chat_session.json'

def load_session_data():
    """Loads session data from the persistence file."""
    if os.path.exists(PERSISTENCE_FILE):
        with open(PERSISTENCE_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Handle cases where the file might be empty or corrupted
                return {}
    return {}

def save_session_data(data):
    """Saves session data to the persistence file."""
    with open(PERSISTENCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_user_context(user_id):
    """Retrieves user-specific context from loaded session data."""
    session_data = load_session_data()
    return session_data.get(user_id, {}) # Return empty dict if user not found

def update_user_context(user_id, key, value):
    """Updates a specific piece of context for a user and saves."""
    session_data = load_session_data()
    if user_id not in session_data:
        session_data[user_id] = {}
    session_data[user_id][key] = value
    save_session_data(session_data)

def simulate_chat_interaction(user_id, user_input):
    """Simulates a chat interaction, demonstrating persistence."""
    print(f"\nUser {user_id} says: {user_input}")

    # Load existing context for the user
    user_context = get_user_context(user_id)

    # Simulate bot logic based on context and input
    if 'last_topic' in user_context:
        print(f"Bot: Welcome back! Last time we talked about {user_context['last_topic']}.")
        if 'order_id' in user_context:
            print(f"Bot: Your order {user_context['order_id']} is being processed.")
    else:
        print("Bot: Hello! How can I help you today?")

    # Update context based on the current interaction
    if "weather" in user_input.lower():
        update_user_context(user_id, 'last_topic', 'weather')
        print("Bot: I can help with weather inquiries.")
    elif "order" in user_input.lower():
        # Simulate extracting an order ID
        order_id = "#12345"
        update_user_context(user_id, 'last_topic', 'orders')
        update_user_context(user_id, 'order_id', order_id)
        print(f"Bot: I've noted your interest in order {order_id}.")
    else:
        update_user_context(user_id, 'last_topic', 'general')

    print(f"Bot: Current context for {user_id}: {get_user_context(user_id)}")

if __name__ == "__main__":
    # Clean up previous session file for a fresh start if it exists
    if os.path.exists(PERSISTENCE_FILE):
        os.remove(PERSISTENCE_FILE)
        print(f"Removed existing {PERSISTENCE_FILE} for a clean run.")

    user_id_alice = "alice"
    user_id_bob = "bob"

    # First interaction for Alice
    simulate_chat_interaction(user_id_alice, "What's the weather like today?")

    # First interaction for Bob
    simulate_chat_interaction(user_id_bob, "I need to check my order status.")

    # Second interaction for Alice, demonstrating persistence
    simulate_chat_interaction(user_id_alice, "Thanks! What about my order?")

    # Third interaction for Bob, demonstrating persistence
    simulate_chat_interaction(user_id_bob, "Can you tell me about the weather?")

    # Load and print final state to show persistence across script runs (conceptually)
    print("\n--- Final Session State --- ")
    final_session_data = load_session_data()
    print(json.dumps(final_session_data, indent=4, ensure_ascii=False))
