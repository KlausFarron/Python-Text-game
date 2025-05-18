# Aleksandr Donovan

# Welcome message and commands for the game
print("Welcome to the Lykaios Knight Adventure Game!")
print("Your goal is to navigate through the castle, collect items, and defeat the Free Magic Creature.")
print("Move commands: go North, go South, go East, go West")
print("Add to inventory: get 'item name'")
print("To use lever: use lever")
print("Type 'exit' to quit the game.")
print("After the floor crumbled, you find yourself in the lower levels.")

# Initialize game state
current_room = "Collapsed Floor Room"
inventory = []
lever_pulled = False
lever_pulled_states = {"Great Hall": False, "Cellar": False}  # Track each lever's state
sealed_room_notified = False  # Flag to track if the player was notified about the sealed room
previous_room = None  # Track the previous room

# Room connections (I Preferred these separated from items and levers)
rooms = {
    "Collapsed Floor Room": {"West": "Hallway"},
    "Hallway": {"East": "Collapsed Floor Room", "West": "Great Hall"},
    "Great Hall": {"North": "Study", "East": "Hallway", "South": "Armory", "West": "Sealed Room"},
    "Study": {"South": "Great Hall", "West": "Library"},
    "Library": {"East": "Study"},
    "Armory": {"North": "Great Hall", "East": "Cellar"},
    "Cellar": {"West": "Armory"},
    "Sealed Room": {"East": "Great Hall"}
}

# Items in rooms
items = {
    "Collapsed Floor Room": None,  # Staring with no items
    "Hallway": "Sword",
    "Library": "Amulet",
    "Study": "Bandages",
    "Armory": "Extra Sword",
    "Great Hall": None,  # Levers are not an item to pick up
    "Cellar": None,
    "Sealed Room": None  # Boss room
}

# Levers in rooms
levers = {
    "Great Hall": "lever",
    "Cellar": "lever",
}

# Lever state at the start
lever_states = {
    "Great Hall": False,
    "Cellar": False,
}

# player status function
def show_status():
    print("\n=== Current Status ===")
    # Display current room
    print("You are in the", current_room)

    # Display inventory
    print("Inventory:", inventory)

    # Check for items in the current room
    if items[current_room] is not None:
        print("You see a", items[current_room])

    # Check for levers in the current room
    if current_room in levers:
        print("You see a lever.")

    # Display available directions
    available_directions = ", ".join(rooms[current_room].keys())
    print("Available directions:", available_directions)
    print("======================\n")

# Function to check if all items are collected
def all_items_collected():
    if "Sword" in inventory and "Extra Sword" in inventory and "Amulet" in inventory and "Bandages" in inventory:
        return True
    else:
        return False

# Function to check if the player input is valid
def valid_command(command):
    return command.startswith("go ") or command.startswith("get ") or command.startswith("use ")

# Function to handle getting an item
def handle_get_command(command):
    global items, current_room
    item_name = command[4:]  # Extract item name after "get "
    if items[current_room] == item_name:
        inventory.append(item_name)
        items[current_room] = None
        print(f"{item_name} retrieved!")
        if all_items_collected():
            print("You have collected all the items! You are ready to face the Free Magic Creature.")
    else:
        print(f"There is no {item_name} here to get.")

# Function to handle using lever
def handle_use_command(command):
    global lever_states, rooms, current_room
    if command == "use lever" and current_room in levers:
        if not lever_states[current_room]:
            print("You pull the lever. You hear a distant sound of stone grinding!")
            lever_states[current_room] = True

            # Check if both levers have been pulled
            if all(lever_states.values()):
                rooms["Sealed Room"]["West"] = "Great Hall"  # Unlock Sealed Room
                print("The Sealed Room is now accessible!")
        else:
            print("The lever in this room has already been pulled.")
    else:
        print("There is no lever to use in this room.")

# Game loop
while True:
    show_status() # shows player status after moving or doing an action

    if current_room == "Sealed Room":
        if not all_items_collected() or not all(lever_states.values()):
            missing = []
            if not all_items_collected():
                missing.append("collect all required items")
            if not all(lever_states.values()):
                missing.append("pull both levers")
            print(f"The room is sealed! You need to {', and '.join(missing)} before you can enter.")

            if previous_room:
                current_room = previous_room
                print(f"You return to the {previous_room}.")
            else:
                current_room = "Great Hall"  # Default fallback
                print("You return to the Great Hall.")
            continue  # Skip the rest of the loop

    # Player inputs
    user_input = input("Enter your move (e.g., 'go North') or 'get <item>', or 'use <object>'. Type 'exit' to quit: ")

    # Check if the player wants to exit the game
    if user_input.lower() == "exit" or user_input.lower() == "quit":
        print("Exiting the game. Goodbye!")
        break  # Exit the game loop

    # Check if the input is valid
    if not valid_command(user_input):
        print("Invalid input! Commands must start with 'go ', 'get ', or 'use '.")
        continue  # Skip the rest of the loop and ask for input again

    # If the input starts with "go"
    if user_input.startswith("go "):
        direction = user_input[3:]

        # Check if the direction is valid for the current room
        if direction in rooms[current_room]:
            next_room = rooms[current_room][direction]

            # Move to the next room
            if next_room is not None:
                current_room = next_room
                print(f"You moved to the {current_room}")
            else:
                print("You can't go that way!")
        else:
            print("Invalid direction!")

    # If the input starts with "get"
    elif user_input.startswith("get "):
        handle_get_command(user_input)
        sealed_room_notified = False  # Resets notification flag when items change

    # If the input starts with "use"
    elif user_input.startswith("use "):
        handle_use_command(user_input)

    # Check win condition
    if current_room == "Sealed Room" and all_items_collected() and all(lever_states.values()):
        print("You have collected all the items and pulled both levers!")
        print("You are ready to face the Free Magic Creature. You win!")
        print("Thank you for playing. I hope you enjoyed the game!")
        break  # Exit the game loop
