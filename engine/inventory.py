"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 20 April 2021
This file is design for inventory purpose, including add/store/delete usages
"""


class Inventory(object):
    def __init__(self, player):
        self.player = player

        self.storage = {}

    def get(self, item_name):
        return self.storage.get(item_name)
    
    def add(self, item_name, number=1):
        """Add item to inventory"""
        if self.get(item_name):
            self.storage[item_name] = self.storage[item_name] + number
        else:
            self.storage[item_name] = number
    
            