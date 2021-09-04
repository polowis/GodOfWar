#!/usr/local/bin/python3
"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 20 April 2021
Inherit from Character class, this class is designed for enemy objects
"""

from entity.character import Character


class Enemy(Character):
    def __init__(self, name, scene):
        super().__init__(name, scene)
        self.base_attack = 5
        self.base_health = 500
        self.level = 1
        self.base_defense = 10

        self.hp_growth = 2
        self.mana_growth = 1
        self.attack_growth = 1
        self.defense_growth = 1

        self.defense = 10
        self.magic = 0
        self.health_growth = 2
        self.max_health = self._get_max_health()
        self.max_mana = 60
        self.health = self.max_health
        self.mana = self.max_mana
        self.skills = ['attack']
        self.exp = 20  # default experience points
        self.coin = 10  # default coins
        
    def fight(self, player):
        self.attack(player)

    @property
    def atk(self):
        return self.base_attack + self.level + self.attack_growth
    
    def _get_max_health(self):
        return int(self.level * self.health_growth + self.base_health)