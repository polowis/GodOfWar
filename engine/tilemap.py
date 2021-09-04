"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 23 April 2021
This file is for creating a console map, responsible for handling character movement
and encoutering monsters
Files read: map.json, mobs.json
"""

import json
import random
from entity.constants import ENEMY_OBJECTS
from engine.battle import Battle


MOBS_RARITY_CHANCE = {
    'common': 0.6,
    'uncommon': 0.25,
    'rare': 0.12,
    'boss': 0.03
}


class Tilemap(object):
    """Construct a tilemap object that is responsible for map drawing and movement functions"""
    def __init__(self, player, scene, map_file: str, map_level: int, blocked_objects=['■']):
        self.player = player
        self.scene = scene
        self.map_file = map_file
        self.map_level = map_level
        self.blocked_objects = blocked_objects

        self.player_symbol = '◉'
        self.pathway_symbol = '□'

        # current coordinates of entity
        self.current_x = 0
        self.current_y = 0

        self.mob_spawn_rate = 30
        self.mob_holders = []  # cached purpose

        self.mob_data = {}
    
    def construct(self):
        """
        Construct the text based map. This will load JSON map file provided

        It will also try to locate the charater position in the map. Return at position (0, 0)
        if no player postion found.
        """
        with open(self.map_file, 'r') as f:
            data = json.load(f)
            for i in data['map']:
                if i['mapLevel'] == self.map_level:
                    self.map_grid = i['grid']
        
        self.locate_player_position()
        self.load_mobs()
    
    def set_player_symbol(self, symbol):
        """Set the character that symbolises player on the map"""
        self.player_symbol = symbol
        return self
    
    def set_pathway_symbol(self, symbol):
        """
        Set the character that symbolises pathway (walkable area) on the map"""
        self.pathway_symbol = symbol
        return self
    
    @property
    def player_position(self):
        """return the player position as tuple formatted: (x_position, y_position)"""
        return (self.current_x, self.current_y)
    
    def locate_player_position(self):
        """Locate the player postion and update the current position of the player"""
        x = 0
        y = 0

        for i in range(len(self.map_grid)):
            for j in range(len(self.map_grid[i])):
                if self.map_grid[i][j] == self.player_symbol:
                    y = i
                    x = j

        self.current_x = x
        self.current_y = y
        return None
    
    def display_current_map(self):
        """
        Display the current map

        Note: This is the current map not the original map
        """
        for grid in self.map_grid:
            self.scene.write(grid)
        self.scene.write("")

    def cannot_move(self, x, y) -> bool:
        """Return boolean value whether or not the given coordinate is allowed to go through"""
        return self.map_grid[y][x] in self.blocked_objects

    def move_player_right(self):
        """Move the entity to the right of the map by 1 step"""
        if self.cannot_move(self.current_x + 1, self.current_y):
            self.scene.write("\n You cannot go that way")
            self.display_current_map()
        else:
            self.update_map_data(self.current_x, self.current_y, self.pathway_symbol)
            self.update_map_data(self.current_x + 1, self.current_y, self.player_symbol)
            self.current_x += 1
            self.display_current_map()
        
        return self

    def move_player_left(self):
        """Move the entity to the left of the map by 1 step"""
        if self.cannot_move(self.current_x - 1, self.current_y):
            self.scene.write(" \n You cannot go that way")
            self.display_current_map()
        else:
            self.update_map_data(self.current_x, self.current_y, self.pathway_symbol)
            self.update_map_data(self.current_x - 1, self.current_y, self.player_symbol)
            self.current_x -= 1
            self.display_current_map()
        
        return self

    def move_player_up(self):
        """Move the entity to the top of the map by 1 step"""
        if self.cannot_move(self.current_x, self.current_y - 1):
            self.scene.write("\n You cannot go that way")
            self.display_current_map()
        else:
            self.update_map_data(self.current_x, self.current_y, self.pathway_symbol)
            self.update_map_data(self.current_x, self.current_y - 1, self.player_symbol)
            self.current_y -= 1
            self.display_current_map()
        
        return self

    def move_player_down(self):
        """Move the entity to the bottom of the map by 1 step"""
        if not self.cannot_move(self.current_x, self.current_y + 1):
            self.scene.write("\n You cannot go that way!!")
            self.display_current_map()
        else:
            self.update_map_data(self.current_x, self.current_y, self.pathway_symbol)
            self.update_map_data(self.current_x, self.current_y + 1, self.player_symbol)
            self.current_y += 1
            self.display_current_map()
        
        return self

    def update_map_data(self, x_value, y_value, value_to_update):
        """Update data at given coordinate"""
        self.map_grid[y_value][x_value] = value_to_update
        return None
    
    def load_mobs(self):
        """Open mobs.json file and load the appropriate mobs into python dictionaries for performance purpose."""
        with open('data/mobs.json', 'r') as file:
            data = json.load(file)
            for i in data['mobs_rarity']:
                if i['map_level'] == self.map_level:
                    self.mob_rarity = i
            
            for mob in data['mobs']:
                if mob['name'] in self.mob_rarity.values():
                    self.mob_holders.append(mob)

            self.mob_data = data
    
    def get_encounter_mob_name(self):
        """Return an enemy name"""
        rarity_type = random.choices(list(MOBS_RARITY_CHANCE.keys()), list(MOBS_RARITY_CHANCE.values()), k=1)[0]
        return self.mob_rarity[rarity_type]
    
    def create_mob(self, mob_name):
        """
        Create an enemy object
        """
        for mob in self.mob_holders:
            if mob['name'] == mob_name:
                enemy_class = ENEMY_OBJECTS[mob['class'].lower()]
                enemy = enemy_class(mob_name, self.scene)
                enemy.exp = random.randint(mob['min_exp'], mob['max_exp'])
                return enemy
    
    def start_battle(self):
        """Start battle"""
        number_of_mob = random.randint(1, 3)
        mob_list = []
        for i in range(number_of_mob):
            mob_name = self.get_encounter_mob_name()
            if mob_name is not None:
                mob = self.create_mob(mob_name)
                mob_list.append(mob)
        battle = Battle(self.player, mob_list, self.scene)
        battle.set_mob_data(self.mob_data)
        battle.begin()

        return None

    @property
    def encounter_mobs(self):
        """Return boolean value whether or not the player encounters monster"""
        return random.randint(1, 100) <= self.mob_spawn_rate

