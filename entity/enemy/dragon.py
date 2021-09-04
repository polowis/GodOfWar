"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 20 April 2021
Inherit from Enemy class, this class is for individual enemy object
"""

from entity.enemy.base import Enemy
import random


class Dragon(Enemy):
    def __init__(self, name, scene):
        super().__init__(name, scene)
        self.base_attack = 25
        self.defense = 10
        self.magic = 20
        self.base_health = 500
        self.max_mana = 100
        self.max_health = self._get_max_health()
        self.health = self.max_health
        self.mana = self.max_mana
        self.skills = ['attack', 'charge', 'bite']
        self.int = 15
        self.str = 10
    
    def fight(self, player):
        if player.health * 100 / player.max_health > 50:
            skill_rate = random.randint(1, 2)
            if skill_rate == 1:
                self.use_charge(player)
            elif skill_rate == 2:
                self.use_bite(player)
        else:
            self.use_attack(player)