"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 20 April 2021
Inherit from Player class, this class is for individual player job
"""

from entity.player.base import Player


class Wizard(Player):
    def __init__(self, name, scene):
        super().__init__(name, scene)
        self.base_attack = 10
        self.attack_growth = 2
        self.defense = 5
        self.magic = 40
        self.max_mana = 60
        self.base_health = 150
        self.max_health = self._get_max_health()
        self.health = self.max_health
        self.mana = self.max_mana
        self.health_growth = 1
        self.skills = ['attack', 'fireball', 'lightningbolt']
        self.int = 15
        self.magic_defense = 10