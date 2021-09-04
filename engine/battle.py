"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 23 April 2021
This file is for initializing battles
"""

import time
import json
import random

MOBS_DROP_RATIRY = {
    "common": 0.6,
    "uncommon": 0.25,
    "rare": 0.12,
    "superrare": 0.03
}


class Battle:
    """
    Create a battle. This will generate its own battle log.
    All other methods that print on screen will be paused

    @param player: Player entity
    
    @param enemies: List of entities

    @param scene: The current scene which must also implements
    the write method to print to screen
    """
    def __init__(self, player, enemies, scene):
        self.player = player
        self.enemies = enemies
        self.scene = scene
        self.turn = 1
        self.wins = 0
        self.kills = 0
        self.exp = 0
        self.player_won = False
        self.battle_end = False
        self.mob_data = {}
    
    def set_mob_data(self, data):
        """Set mob data"""
        self.mob_data = data
        return self

    def get_mob_data(self):
        """
        Get mob data
        
        If no data is set, it will set it. Default file is mobs.json
        """
        if self.mob_data:
            return self.mob_data

        with open('data/mobs.json', 'r') as file:
            data = json.load(file)
            self.mob_data = data
        
        return self.mob_data
    
    def get_mob_drop_by_name(self, name):
        """Get item drop from mob name"""
        data = self.get_mob_data()
        rarity_type = random.choices(list(MOBS_DROP_RATIRY.keys()), list(MOBS_DROP_RATIRY.values()), k=1)[0]

        for mob in data['mobs']:
            if mob['name'] == name:
                return mob[rarity_type]

    def begin(self):
        while not self.player_won and not self.battle_end:
            self.scene.write(f"Turn {self.turn}: \n")

            self.perform_player_actions()
            self.turn += 1
            self.perform_enemy_actions()
            
    def get_player_action(self):
        try:
            self.scene.write("1. Fight")
            self.scene.write("2. Escape")
            self.scene.window.wait_variable(self.scene.input)
            choice = self.scene.input.get()

            if choice == 'quit':
                self.scene.window.quit()

            if int(choice) not in range(1, 3):
                raise ValueError()

            return int(choice)
        except ValueError:
            self.scene.write("Invalid command please type again \n")
            self.get_player_action()
    
    def get_player_skill(self):
        """Prompt user to select skill"""
        self.scene.write("\n Please select your skill:")
        try:
            for i in range(len(self.player.skills)):
                self.scene.write(f"{i}. {self.player.skills[i]}")
            self.scene.window.wait_variable(self.scene.input)
            choice = self.scene.input.get()

            if choice == 'quit':
                self.scene.window.quit()

            skill_name = self.player.skills[int(choice)]
            return skill_name
        except IndexError:
            self.scene.write("Invalid command please type again \n")
            self.get_player_skill()
    
    def choose_target(self):
        """Promt user to choose enemy"""
        try:
            self.scene.write("Choose your target:")
            for enemy_index in range(len(self.enemies)):
                if not self.enemies[enemy_index].is_dead:
                    self.scene.write(str(enemy_index) + ". " + self.enemies[enemy_index].name)
            self.scene.write("")
            self.scene.window.wait_variable(self.scene.input)
            target = self.scene.input.get()

            if target == 'quit':
                self.scene.window.quit()

            target = int(target)
            if not (target < len(self.enemies) and target >= 0) or self.enemies[target].health <= 0:
                raise ValueError
            return self.enemies[target]
        except ValueError:
            self.scene.write("You must enter a valid choice \n")
            return self.choose_target()

    def perform_enemy_actions(self):
        """Do enemy action. This will call the fight method that is implemented by child character class"""
        if not self.player_won:
            self.scene.write("Enemies' turn:")
            time.sleep(1)
            for enemy in self.enemies:
                if not enemy.is_dead:
                    enemy.fight(self.player)
                    if self.player.is_dead:
                        self.battle_end = True
                        self.player_won = False
                        break
            if self.battle_end:
                self.scene.write("You have been killed by your enemy")
                self.player.reset_stats()
    
    def display_enemy_status(self):
        """print enemy current status"""
        for enemy in self.enemies:
            enemy.display_current_status()
        self.scene.write("")

    def perform_player_actions(self):
        """
        This method must be called every battle

        Usually, you don't need to call this method explicitly
        """
        turn_over = False

        self.display_enemy_status()
        
        while not turn_over and not self.player_won:

            self.player.display_current_status()

            player_action = self.get_player_action()

            if player_action == 1:
                skill_choice = self.get_player_skill()
                target = self.choose_target()
                self.player.use_skill(skill_choice, target)

                time.sleep(1)

                if target.is_dead:
                    self.kills += 1
                    self.player.exp += target.exp
                    item_drop_name = self.get_mob_drop_by_name(target.name)
                    self.scene.write("You got {}".format(item_drop_name))
                    self.player.inventory.add(item_drop_name)
                    self.scene.write('\n You received {} experience points \n'.format(target.exp))
                    if self.player.can_level_up():
                        self.player.level_up()
                        self.player.reset_stats()

            elif player_action == 2:
                self.scene.write("You have successfully escaped from the battle")
                self.player_won = True
                self.battle_end = True
                return

            turn_over = True
            self.player_won = True

            for enemy in self.enemies:
                if enemy.health > 0:
                    self.player_won = False
                    break
            if self.player_won:
                self.scene.write("Your enemies have been slained")

