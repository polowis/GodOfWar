"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 21 April 2021
This file stores constant variables related to Character object and utility functions
"""

from entity import Wizard, Sniper, Assassin
from entity import Dragon, Savager, Goblin, Megaroche

CHARACTER_JOB_OBJECTS = {
    'assassin': Assassin,
    'sniper': Sniper,
    'wizard': Wizard
}

ENEMY_OBJECTS = {
    'savager': Savager,
    'dragon': Dragon,
    'goblin': Goblin,
    'megaroche': Megaroche
}


def create_character(job_name: str, character_name: str, scene):
    job_obj = CHARACTER_JOB_OBJECTS.get(job_name.lower().strip())
    return job_obj(character_name, scene)