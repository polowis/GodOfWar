#!/usr/local/bin/python3
"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 20 April 2021
Inherit from Character class, this class is designed for player objects
"""

from entity.character import Character


class Player(Character):
    def __init__(self, name, scene):
        super().__init__(name, scene)
        self.hp_growth = 1
        self.mana_growth = 1
        self.attack_growth = 1
        self.defense_growth = 1
        self.base_attack = 10
        self.attack_score = 2
        self.defense_score = 1
        self.defense = 3
        self.magic = 0
        self.base_health = 100
        self.max_mana = 60
        self.health = self.max_health
        self.mana = self.max_mana
        self.skills = ['attack']
    
    @property
    def atk(self):
        return self.base_attack