import time
import random

def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def intro():
    print_slow("Welcome to Dragon Quest!")
    print_slow("In this adventure, you are a brave knight on a quest to defeat the dragon terrorizing the kingdom.")
    print_slow("Your journey begins now...\n")
    time.sleep(1)

def choose_weapon():
    print_slow("Before you embark on your quest, choose your weapon:")
    print("1. Sword")
    print("2. Bow and Arrows")
    print("3. Magic Staff")
    
    while True:
        choice = input("Enter the number of your choice: ")
        if choice in ["1", "2", "3"]:
            if choice == "1":
                weapon = "Sword"
            elif choice == "2":
                weapon = "Bow and Arrows"
            else:
                weapon = "Magic Staff"
            print_slow(f"You've chosen the {weapon}! Prepare for your journey...\n")
            return weapon
        else:
            print("Please enter a valid choice (1, 2, or 3).")

def encounter_dragon(weapon):
    print_slow("You approach the dragon's lair...")
    print_slow("The dragon emerges from the shadows, breathing fire!")
    print_slow(f"You brandish your {weapon} and prepare for battle.\n")
    time.sleep(1)
    
    dragon_health = 50
    player_health = 30
    
    while dragon_health > 0 and player_health > 0:
        print(f"Dragon Health: {dragon_health}\tYour Health: {player_health}")
        print("What do you do?")
        print("1. Attack")
        print("2. Defend")
        print("3. Retreat")
        
        choice = input("Enter the number of your choice: ")
        
        if choice == "1":
            damage = random.randint(5, 10)
            print_slow(f"You attack the dragon with your {weapon} and deal {damage} damage!")
            dragon_health -= damage
        elif choice == "2":
            block = random.randint(1, 5)
            print_slow(f"You brace yourself and defend against the dragon's attack, reducing incoming damage.")
            player_health -= max(0, 8 - block)
        elif choice == "3":
            print_slow("You retreat from the battle... Cowardice is not an option!")
            player_health -= 5
        
        if dragon_health > 0:
            dragon_damage = random.randint(6, 12)
            print_slow(f"The dragon attacks you with its fiery breath and deals {dragon_damage} damage!")
            player_health -= dragon_damage
        
        if player_health <= 0:
            print_slow("You have been defeated by the dragon. Game Over!")
            return False
        elif dragon_health <= 0:
            print_slow("Congratulations! You have defeated the dragon and saved the kingdom!")
            return True

def play_game():
    intro()
    weapon = choose_weapon()
    result = encounter_dragon(weapon)
    
    if result:
        print_slow("Thank you for playing Dragon Quest!")
    else:
        print_slow("Better luck next time. You can try again!")

if __name__ == "__main__":
    play_game()
