
import sys
import random
import time

name = input("What is your name? ").strip()


def main():
    # Game Start and character customization
    current_node = root
    print(f"{current_node.text}")
    print("Choose your starting weapon:")
    for i in range(len(current_node.reward)):
        print(f"Choose weapon: {current_node.reward[i].name}, "
              f"Power: {current_node.reward[i].power}, "
              f"Accuracy: {current_node.reward[i].accuracy}")
    while True:
        check = False
        answer = input("Select weapon: ").lower().strip()
        for item in range(len(current_node.reward)):
            if answer != current_node.reward[item].name.lower():
                check = False
                continue
            else:
                check = True
                break
        if check:
            break
        else:
            print("Please select a valid weapon")
    weapon_inventory.append(answer)
    if answer in str(current_node.reward[0]).lower():
        winventory.update({answer: current_node.reward[0]})
    elif answer in str(current_node.reward[0]).lower():
        winventory.update({answer: current_node.reward[1]})
    else:
        winventory.update({answer: current_node.reward[2]})

    # Beginning of gameplay loop
    while not current_node.end:
        while True:
            choice = input(f"{current_node.prompt}").lower().strip()
            if choice not in ["a", "b"]:
                print("Please pick a valid choice")
            else:
                break
        if choice == "a":
            current_node = current_node.left
        else:
            current_node = current_node.right
        print(current_node.text)
        while True:
            answer = input(f"You see one {current_node.food.name}, do you want to inspect it? ").lower().strip()
            if answer not in ("y", "yes", "n", "no"):
                print("Please say Yes or No")
            else:
                break
        if answer in ("y", "yes"):
            current_node.food.inspect()
            while True:
                answer = input(f"Do you want to take the {current_node.food}? ")
                if answer not in ("y", "yes", "n", "no"):
                    print("Please say Yes or No")
                else:
                    break
            if answer in ("y", "yes"):
                food_inventory.append(current_node.food)
                finventory.update({str(current_node.food).lower(): current_node.food})
                current_node.food.item_get()
        for monster in range(len(current_node.enemies)):
            combat(current_node.enemies[monster])
            time.sleep(1)
        print(f"{player.name} finds three treasure chests: ")
        for option in range(len(current_node.reward)):
            print(f"{current_node.reward[option].name}, "
                  f"Power: {current_node.reward[option].power},"
                  f"Accuracy: {current_node.reward[option].accuracy}")
        while True:
            check = False
            answer = input("Select one treasure to take with you: ").lower().strip()
            for item in range(len(current_node.reward)):
                if answer != current_node.reward[item].name.lower():
                    check = False
                    continue
                else:
                    check = True
                    break
            if check:
                break
            else:
                print("Please select a valid reward")
        weapon_inventory.append(answer)
        if answer in str(current_node.reward[0]).lower():
            winventory.update({answer: current_node.reward[0]})
        elif answer in str(current_node.reward[0]).lower():
            winventory.update({answer: current_node.reward[1]})
        else:
            winventory.update({answer: current_node.reward[2]})
    print("You Win! Try to defeat all four of the Dragon King's Generals!")
    sys.exit()


class Entity:
    def __init__(self, Name, HP, Power, Accuracy, Exp, Flee_Chance):
        self.name = Name
        self.hp = HP
        self.power = Power
        self.accuracy = Accuracy
        self.exp = Exp
        self.flee_chance = Flee_Chance

    def is_alive(self):
        if self.hp <= 0:
            print(f"{self.name} has fallen." "Game Over! \n Exiting Game...")
            sys.exit()

    def flee(self, enemy):
        if random.uniform(0, enemy.flee_chance) <= self.flee_chance:
            return True
        return False

    def attack(self, weapon, target):
        if weapon is None:
            total_damage = self.power
            total_hit = self.accuracy
        else:
            total_damage = weapon.power + self.power
            total_hit = weapon.accuracy + self.accuracy
        if random.random() <= total_hit:
            time.sleep(.5)
            print("Hit!")
            target.hp -= total_damage
            if target.hp <= 0:
                print(f"{target.name} has fallen")
                return
            else:
                print(f"{target.name} has {target.hp} HP left!")
        else:
            print("Miss!")


class Character(Entity):
    def __init__(self, Name, Level, MaxHP, HP, Power, Accuracy, Exp, Flee_Chance):
        Entity.__init__(self, Name, HP, Power, Accuracy, Exp, Flee_Chance)
        self.level = Level
        self.max_hp = MaxHP

    def recover(self, food):
        self.hp = min(self.max_hp, food.recovery + self.hp)
        print(f"Your HP is now {self.hp}")

    def experience(self, enemy):
        print(f"You have gained {enemy.exp} experience points.")
        self.exp += enemy.exp
        if self.exp >= 100:
            self.level += 1
            self. max_hp += 20
            self.power += 10
            self.accuracy += .10
            self.hp = self.max_hp
            self.exp -= 100
            print("Congratulations! You have leveled up!")
            print(f"Stats - Level: {self.level}, "
                  f"HP: {self.max_hp}, "
                  f"Power: {self.power}, "
                  f"Accuracy: {self.accuracy}, ")


class Enemy(Entity):
    def __init__(self, Name, HP, Power, Accuracy, Exp, Flee_Chance):
        Entity.__init__(self, Name, HP, Power, Accuracy, Exp, Flee_Chance)


class Item:
    def __init__(self, Name):
        self.name = Name

    def __str__(self):
        return "{self.name}".format(self=self)

    def item_get(self):
        print(f"You have picked up {self.name}")

    __repr__ = __str__


class Weapon(Item):
    def __init__(self, Name, Power, Accuracy):
        Item.__init__(self, Name)
        self.power = Power
        self.accuracy = Accuracy


class Food(Item):
    def __init__(self, Name, Recovery):
        Item.__init__(self, Name)
        self.recovery = Recovery

    def inspect(self):
        print(f"Name: {self.name}, Recovery: {self.recovery}")


class Node:
    def __init__(self, value, text, food, enemies, reward, prompt, complete, end):
        self.left = None
        self.right = None
        self.value = value
        self.text = text
        self.food = food
        self.enemies = enemies
        self.reward = reward
        self.prompt = prompt
        self.complete = complete
        self.end = end

    def insert(self, value, text, food, enemies, reward, prompt, complete, end):
        if self.value:
            if value < self.value:
                if self.left is None:
                    self.left = Node(value, text, food, enemies, reward, prompt, complete, end)
                else:
                    self.left.insert(value, text, food, enemies, reward, prompt, complete, end)
            elif value > self.value:
                if self.right is None:
                    self.right = Node(value, text, food, enemies, reward, prompt, complete, end)
                else:
                    self.right.insert(value, text, food, enemies, reward, prompt, complete, end)
        else:
            self.value = value
            self.text = text
            self.food = food
            self.enemies = enemies
            self.prompt = prompt
            self.complete = complete
            self.end = end


# Combat loop
def combat(monster):
    print(f"You have encountered a {monster.name}! What will you do?")
    while monster.hp >= 0:
        while True:
            answer = input("A: Fight | B: Use Food | C: Flee | ").lower().strip()
            if answer not in ["a", "b", "c"]:
                print("Please select A, B, or C")
            else:
                break
        if answer == "a":
            while True:
                answer = input(f"Select weapon: {weapon_inventory} ").lower().strip()
                if answer not in weapon_inventory:
                    print("Please select a valid weapon")
                else:
                    break
            player.attack(winventory[answer], monster)
            if monster.hp <= 0:
                break
        elif answer == "b":
            while True:
                check = False
                answer = input(f"Select item: {food_inventory} ").lower().strip()
                for item in range(len(food_inventory)):
                    if answer != food_inventory[item].name.lower():
                        check = False
                        continue
                    else:
                        check = True
                        break
                if check:
                    break
                else:
                    print("Please select a valid item")
            player.recover(finventory[answer])
        elif answer == "c":
            if player.flee(monster):
                print("You have successfully fled!")
                break
            else:
                print("You have failed to flee!")
                continue
        print(f"{monster.name} attacks.")
        time.sleep(1)
        monster.attack(None, player)
        player.is_alive()
    if monster.hp <= 0:
        print(f"{player.name} has slain {monster.name}.")
        player.experience(monster)


# Initializing player character stats with name placeholder
player = Character(name, 1, 100, 100, 20, .10, 0, .30)

# Weapons set up
basic_weapons = [
    Weapon("Bronze Sword", 30, .90),
    Weapon("Bronze Lance", 40, .80),
    Weapon("Bronze Axe", 50, .70)
]
intermediate_weapons = [
    Weapon("Silver Sword", 40, .80),
    Weapon("Silver Lance", 50, .70),
    Weapon("Silver Axe", 60, .60)
]
gold_weapons = [
    Weapon("Gold Sword", 50, .70),
    Weapon("Gold Lance", 60, .60),
    Weapon("Gold Axe", 70, .50)
]

# Populating enemies
ogre = [
    Enemy("Ogre", 100, 10, .75, 40, .50),
    Enemy("Ogre", 100, 10, .75, 40, .50),
    Enemy("Ogre", 100, 10, .75, 40, .50)
]
mushroom = [
    Enemy("Warped Mushroom", 120, 20, .70, 55, .40),
    Enemy("Warped Mushroom", 120, 20, .70, 55, .40),
    Enemy("Warped Mushroom", 120, 20, .70, 55, .40)
]
knight = [
    Enemy("Dragon Knight", 200, 30, .70, 70, 1)
]
wizard = [
    Enemy("Demon Wizard", 160, 35, .60, 75, 1)
]
wolf = [
    Enemy("Blood Wolf", 200, 35, 60, 75, 1)
]
giant = [
    Enemy("Sand Giant", 220, 40, 55, 80, 1)
]

# food stats
apple = Food("Apple", 20)
meat = Food('meat', 30)
potion = Food('potion', 50)
greater_potion = Food('greater potion', 80)
elixir = Food('elixir', 10000)

# Inventory set up
weapon_inventory = []
food_inventory = []
winventory = {}
finventory = {}

# Game route set up
root = Node(4,
            f"Welcome to Novis, {player.name}. You must challenge the Dragon King to save this once peaceful land. "
            f"Please choose your weapon: ",
            None,
            None,
            basic_weapons,
            "To travel to the Dragon King\'s lair, you must travel through "
            "(A) the Dark Woods, or (B) the Swamp of Terror. Which will you choose? ",
            None,
            False)
root.insert(2,
            "You travel to the Dark Woods. The air is chilly and you can barely see in front of you",
            apple,
            ogre,
            intermediate_weapons,
            f"{player.name} has emerged from the Dark Woods! You find a fork in the road. "
            "Do you go to (A) the High Fort, or (B) the Dread Tower? ",
            None,
            False)
root.insert(6,
            "You travel to the Swamp of Terror. The putrid stench fills your nose making it hard to breathe.",
            apple,
            mushroom,
            intermediate_weapons,
            f"{player.name} has emerged from the Swamp of Terror! You find a fork in the road."
            f"Do you go to (A) the Wolf Den, or (B) the Mirage Desert? ",
            None,
            False)
root.insert(1,
            "You travel to the High Fort. The massive structure sits atop a large cliff. ",
            meat,
            knight,
            gold_weapons,
            "The Dragon Knight's forces dissipate into the darkness. The Fort is conquered."
            "Congratulations! You have slain the Dragon King's General. ",
            False,
            True)
root.insert(3,
            "You travel to the Dread Tower. The colossal structure pierces the heavens themselves. ",
            meat,
            wizard,
            gold_weapons,
            "Congratulations! You have slain the Dragon King's General. ",
            False,
            True)
root.insert(5,
            "You travel to the Wolf Den. Bones of its deceased prey cover the ground. ",
            potion,
            wolf,
            gold_weapons,
            "Congratulations! You have slain the Dragon King's General. ",
            False,
            True)
root.insert(7,
            "You travel to the Mirage Desert. Sweat drips quickly down your body and evaporates just as fast. ",
            potion,
            giant,
            gold_weapons,
            "Congratulations! You have slain the Dragon King's General. ",
            False,
            True)

# Run Game
main()
