"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 21 April 2021
Class object for each character. This class stores character attributes,
calculate amount of damages and recived, skill damages.
"""

import random
import time
from engine.inventory import Inventory


class Character(object):
    """A character object"""
    def __init__(self, name, scene):
        self.scene = scene
        self.name: str = name

        self.crit_chance = 2
        self.crit_damage_rate = 1.5
        self.evasion = 5
        self.resistance = 5
        self.level = 1

        self.base_attack = 3
        self.base_health = 100
        self.base_defense = 10
        self.base_magic = 2

        self.hp_growth = 2
        self.mana_growth = 1
        self.attack_growth = 1
        self.defense_growth = 1

        self.defense = 10
        self.magic_defense = 2
        self.magic = 1
        self.melee = 1
        self.health_growth = 1
        self.max_health = self._get_max_health()
        self.max_mana = 60
        self.health = self.max_health
        self.mana = self.max_mana
        self.skills = ['attack']

        # attributes that can be modified by player
        self.str = 1
        self.int = 1
        self.agi = 1
        self.crt = 1

        self.coin = 20
        self.exp = 0
        self.inventory = Inventory(self)

        self.class_name = str(self.__class__.__name__)
    
    class LevelUpError(Exception):
        def __init__(self, message="Unable to level up."):
            super().__init__(self, message)

    def __str__(self):
        """string representation of this character"""
        return str(self.__class__.__name__)

    def job(self):
        return self.job_name
    
    def has_critical_chance(self) -> bool:
        """Return true if this character has chance to do critical attack"""
        critical_chance = random.randint(1, 100)
        return critical_chance <= self.crit_chance

    def use_attack(self, target):
        """Basic attack skill for every class"""
        self.scene.write(f"{self.name} uses attack!")
        attack_roll = random.randint(1, 20)
        raw_damage = int(self.atk * attack_roll * 1.80)

        if self.has_critical_chance():
            raw_damage = raw_damage * self.crit_damage_rate
            self.scene.write(self.name + " dealt critical damage!!")

        is_die = target.defend(raw_damage)
        if is_die:
            target.on_die()
    
    def use_backstab(self, target):
        """Physical attack skill"""
        double_rate = random.randint(1, 100)
        damage_point = 1
        if double_rate <= 30:  # 30% chance to inflict double damage
            damage_point = 2
        
        double_damage_rate = random.uniform(1.7, 2.8)
        self.scene.write(self.name + " 's backstab!!")
        target_def_deduction = target.resistance + target.defense + 100
        damage = round(((self.atk * double_damage_rate * 100) / target_def_deduction) * damage_point * self.crit_damage_rate)
        if damage < 0:
            damage = 1
        time.sleep(1)
        self.scene.write(f"{self.name} dealt {damage} critical damages to {target.name}")
        target.health -= damage
        if target.is_dead:
            target.on_die()
    
    def use_crossfire(self, target):
        """Physical attack skill"""
        number_of_arrows = random.randint(1, 8)
        raw_damage: int = int(self.atk * 5.45 * number_of_arrows * (1 + self.crt / 100))

        self.scene.write(self.name + " crossfires!!")
        if raw_damage < 0:
            raw_damage = 1
        
        is_die = target.defend(raw_damage)
        if is_die:
            target.on_die()
    
    def use_arrowrain(self, target):
        """Physical attack skill for sniper"""
        number_of_arrows = random.randint(1, 6)
        raw_damage: int = int(self.atk * 3.45 * number_of_arrows * 2 * (1 + self.crt / 100))

        self.scene.write(self.name + " arrow rain!!")
        if raw_damage < 0:
            raw_damage = 1
        
        is_die = target.defend(raw_damage)
        if is_die:
            target.on_die()
    
    def use_fireball(self, target):
        """Magical attack skill"""
        raw_damage = (self.magic * 4.65 + self.matk + self.int * 2) * self.rng(1, 9)
        self.scene.write(self.name + " casts fireballs!")
        if raw_damage < 0:
            raw_damage = 1
        
        is_die = target.defend(raw_damage, damage_type='magic')
        if is_die:
            target.on_die()
    
    def use_lightningbolt(self, target):
        """Magical attack skill"""
        raw_damage = (self.magic * 3.45 + self.matk + self.int * 3) * self.rng(3, 7)
        self.scene.write(self.name + " uses lightning bolt!")
        if raw_damage < 0:
            raw_damage = 1
        
        is_die = target.defend(raw_damage, damage_type='magic')
        if is_die:
            target.on_die()
    
    def use_charge(self, target):
        """Physcial attack skill"""
        raw_damage = (self.atk * 4.50 + self.melee + self.str * 2) * self.rng(3, 10)
        if self.has_critical_chance:
            raw_damage = raw_damage * self.crit_damage_rate
        
        self.scene.write(self.name + " charges!!")
        if raw_damage < 0:
            raw_damage = 1
        target.defend(raw_damage)
        if target.is_dead:
            target.on_die()
    
    def use_bite(self, target):
        """Physcial attack skill"""
        raw_damage = (self.atk * 2.50 + (self.melee * 0.80) + self.str * 3) * self.rng(5, 10)
        if self.has_critical_chance:
            raw_damage = raw_damage * self.crit_damage_rate
        
        self.scene.write(self.name + " bites!!")
        if raw_damage < 0:
            raw_damage = 1
        target.defend(raw_damage)
        if target.is_dead:
            target.on_die()
        
    def defend(self, damage, damage_type='physical'):
        """Allows the given entity to evade or reduce damage from incoming hit significantly"""
        evasion_rate = random.randint(1, 100)

        if evasion_rate <= self.evasion:
            self.scene.write(self.name + " dodged the attack")
            return False
        
        random_number_deduction = random.randint(1, 20)  # 20 % of raw damage deduction
        if damage_type == 'physical':
            reduced_damage = int((damage * random_number_deduction / 100) * (100 / (100 + self.defense)))

        elif damage_type == 'magic':
            reduced_damage = int((damage * random_number_deduction / 100) * (100 / (100 + self.magic_defense)))

        if reduced_damage < 0:
            reduced_damage = 1
        self.health = self.health - reduced_damage
        self.scene.write(f"{self.name} suffers {reduced_damage} damages")
        time.sleep(1)

        if self.health <= 0:
            return True

        return False

    def on_die(self):
        """Call this method when the entity dies"""
        self.health = 0
        self.scene.write(f"{self.name} has died. \n")
        time.sleep(1)

    def use_skill(self, skill_name, target=None):
        """
        Use specific skill given the name of the skill. If the skill requires
        target, you must include target entity.
        """
        if target is not None:
            skill = getattr(self, 'use_' + skill_name)(target)

        else:
            skill = getattr(self, 'use_' + skill_name)()
        
        return skill

    def display_current_status(self):
        self.scene.write(
            f"{self.name} has {self.health}/{self.max_health}hp left. {self.mana}/{self.max_mana}mp left.")
    
    @property
    def is_dead(self):
        """Return if this entity is dead"""
        return self.health <= 0
    
    @property
    def atk(self):
        """Return atk attribute, override this method if needed"""
        return int(self.base_attack + self.level + self.attack_growth)
    
    @property
    def matk(self):
        """Return matk attribute, override this method if needed"""
        return int((self.int - 1 + self.base_magic + self.level) * 4)
    
    def _get_max_health(self):
        """Return the maximum health of this entity
        
        Any child class musts call this method in its constructor as follows:

        self.max_health = self._get_max_health()
        """
        return int(self.level * self.health_growth + self.base_health)
    
    def as_dict(self):
        """
        Return this entity attributes as dictionary
        
        Note: This will return all attributes belong to this entity
        """
        return self.__dict__
    
    def as_string(self, hidden_attrs: list = ['scene']):
        """
        Return this entity object as string format

        :param hidden_attrs: List of hidden attributes you wish to hide
        """
        allowed_properties = []
        for i in self.as_dict().items():
            if i[0] not in hidden_attrs:
                allowed_properties.append(("{}: {}".format(*i)))
        
        return '\n'.join(allowed_properties)
    
    def show_character_info_window(self):
        """
        Create a new pop up window and write this entity information out
        """
        hidden_attrs = ['scene', 'inventory', 'skills', 'critical_damage_rate', 'critical_chance']
        return self.scene.window.display_popup_window(self.as_string(hidden_attrs))

    def rng(self, start: int, end: int) -> bool:
        """Return random integer number"""
        return random.randint(start, end)
    
    def load_config(self, **kwargs):
        """Populate this entity attribute by providing dictionary of attributes."""
        try:
            for config_key, config_value in kwargs.items():

                # convert all to numeric number
                if config_value.isnumeric():
                    config_value = int(config_value)
                else:
                    config_value = float(config_value)

                # if valueerror is raise, we do nothing and continue with remaining data
                if isinstance(config_value, str):
                    if config_value.startswith('[') and config_value.endswith(']'):
                        config_value = config_value.strip('[]').replace('\'', '').replace(' ', '').split(',')
                setattr(self, config_key, config_value)

        except AttributeError:
            self.scene.write('Unexpected key')

        except ValueError:
            pass
    
    def get_exp_requried_to_level_up(self):
        """Return the exp required to level up"""
        return int(0.04 * (self.level * 3600))
    
    def can_level_up(self):
        """Return true if this entity can level up"""
        return self.exp >= self.get_exp_requried_to_level_up()
    
    def level_up(self):
        """
        Level up the character and reset the experiences.

        To use this method, consider calling Character.can_level_up first or
        use try catch as this will throw Character.LevelUpError
        """
        if self.can_level_up:
            self.exp = 0 + self.exp - self.get_exp_requried_to_level_up()
            self.level += 1
        else:
            raise Character.LevelUpError()
    
    def reset_stats(self):
        """Reset player stats"""
        self.health = self.max_health
        self.mana = self.max_mana
            
    def print_level_up_message(self):
        """
        Print to the screen level up message
        """
        self.scene.write("Your level have raised to {}".format(self.level))
    
    def set_drop_items(self, items_dict):
        pass

