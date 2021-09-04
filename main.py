"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 17 April 2021
This file is the main entry of the enitre program
Files read: item.json, map.json, mobs.json, user-selected-file.txt
Files write: user-selected-file.txt
"""
from engine import Game

game_config = {
    "screen_wdith": 800,
    "screen_height": 500,
    "number_of_cols": 13,
    "number_of_rows": 13,
    "grid_weight": 1,
    "background": '#2C3E50'
}


def main():
    game = Game(**game_config)
    game.title('Wonderful land')
    game.change_scene(game, 'home')
    game.mainloop()


main()
