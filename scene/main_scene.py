"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 26 April 2021
This file is for display GUI for main scene and handle inputs
"""

from scene.scene_interface import SceneInterface
from tkinter import StringVar
from entity.constants import CHARACTER_JOB_OBJECTS, ENEMY_OBJECTS
from engine.battle import Battle
from engine.shop import Shop
from engine.tilemap import Tilemap


class MainScene(SceneInterface):
    def __init__(self, window):
        self.window = window
        self.input = StringVar()
        self.input.trace('w', self._monitor_input)

        self.player_job = self.window.storage['player_job']
        job_obj = CHARACTER_JOB_OBJECTS.get(self.player_job.lower())
        self.window.storage['authenticated_user'] = job_obj(self.window.storage['player_name'], self)
        self.player = self.window.user

    def run(self):
       
        self._display_UI()

        self.write_welcome_message()

        self._display_text_menu_choices()

    def destroy(self):
        pass

    def _display_UI(self):
        """Display UI for this scene"""
        self._display_text_widget()

        self._display_input_bar()

        self._display_menu_side()

    def write(self, message):
        """Write message to screen"""
        self.text_window.write(message)
    
    def _monitor_input(self, *args):
        pass

    def _display_text_widget(self):
        self.text_scrollbar = self.window.add.scrollbar()
        self.text_scrollbar.grid(row=0, column=2, sticky='NS')

        self.text_window = self.window.add.text()
        self.text_window.grid(column=0,
                              row=0,
                              columnspan=3,
                              sticky='NSEW')

        self.text_scrollbar.config(command=self.text_window.text.yview)
        self.text_window.text['yscrollcommand'] = self.text_scrollbar.scrollbar.set

    def _display_text_menu_choices(self):
        self.write("\n")
        try:
            self.write("Please choose what you would like to do:")
            self.write("1. Start a battle")
            self.write("2. Map Adventure")

            self.window.wait_variable(self.input)

            choice = self.input.get()

            if choice == 'quit':
                self.window.quit()

            if int(choice) == 1:
                return self.start_battle()

            elif int(choice) == 2:
                return self.init_map()

        except (ValueError, TypeError) as e:
            print(e)
            self.write("invalid value, please enter again")
            self._display_text_menu_choices()

    def _display_menu_side(self):
        self.exit_button = self.window.add.button(text="Exit the game", command=self._quit)
        self.exit_button.button.place(x=670, y=100)

        self.save_button = self.window.add.button(text="Save the game", command=self.save_game)
        self.save_button.button.place(x=670, y=140)

        self.load_button = self.window.add.button(text='Load saved game', command=self.load_game)
        self.load_button.button.place(x=670, y=180)

        self.show_info_button = self.window.add.button(text="Show info", command=self.show_character_info)
        self.show_info_button.place(x=670, y=220)

        self.shop_button = self.window.add.button(text="Shop", command=self.go_to_shop)
        self.shop_button.place(x=670, y=260)
    
    def show_character_info(self):
        return self.player.show_character_info_window()
    
    def load_game(self):
        file_path = self.window.open_file()
        if file_path is None:
            return
        try:
            saved_attrs = {}
            with open(file_path, 'rb') as file:
                for line in file.readlines():
                    line = line.decode('utf-8')
                    key, value = line.rstrip('\r\n').split(": ")
                    saved_attrs[key] = value
                
                player_class = CHARACTER_JOB_OBJECTS.get(saved_attrs['class_name'].lower())
                player_object = player_class(saved_attrs['name'], self)
                player_object.load_config(**saved_attrs)

                self.window.user = player_object

                self.player = player_object

                self.window.current_file_path = file_path

                self.write(f"You are now playing as the {self.player.name}, the {self.player.class_name}")

                self.window.title(file_path + ' Wonderful Land')

        except FileNotFoundError:
            return
    
    def save_game(self):
        """Save the game process"""
        if self.window.current_file_path:
            try:
                with open(self.window.current_file_path, 'wb') as file:
                    file.write(self.player.as_string().encode('utf-8'))
                    return
            except FileNotFoundError:
                self.write("File does not exist")
                return
        else:
            file_path = self.window.save_file()
            if file_path is None:
                return
            try:
                with open(file_path, 'wb') as file:
                    file.write(self.player.as_string().encode('utf-8'))
                    self.window.storage['current_saved_file_path'] = file_path
            except FileNotFoundError:
                self.write("File does not exist")
                return

    def go_to_shop(self):
        shop = Shop(self.player, self)
        shop.enter()

    def _quit(self):
        self.input.set('quit')
        self.window.quit()

    def _display_input_bar(self):
        self.message_entry = StringVar()
        self.message_entry_bar = self.window.add.input(textvariable=self.message_entry)
        self.message_entry_bar.grid(column=0, row=1, sticky='SEW', columnspan=3)

        self.message_entry_bar.entry.focus_set()

        self.message_entry_bar.entry.bind("<Return>", self.on_enter_input)

    def write_welcome_message(self):
        self.write(f"Hello {self.window.user.name}!, welcome to wonderful land. \n")
        self.write("Wonderful land is a text based RPG game developed by Hung Tran")
        self.write("You are an adventurer, explore the game while you can. All the menu options are on the right")
        self.write("Please follow the game instruction closely")
        self.write("Start map adventure to freely move your character, you can always go back!")
        self.write(f"You are the {self.window.user}. Each job you choose will have different stats")
        self.write("Explore all the options!. Make sure to save and load the game so you don't lose your progress")

    def on_enter_input(self, event):
        self.input.set(self.message_entry.get())
        self.message_entry.set('')

    def start_battle(self):
        enemies = [ENEMY_OBJECTS['dragon']('Ether', self)]
        battle = Battle(self.player, enemies, self)
        battle.begin()

        return self._display_text_menu_choices()
    
    def init_map(self):
        self.tilemap = Tilemap(self.player, self, 'data/map.json', 1)
        self.tilemap.construct()
        self.tilemap.display_current_map()
        return self._display_movement_opt_menu()
    
    def _display_movement_opt_menu(self):
        """Display menu option to perform player movement"""
        try:
            self.write('A. Move left')
            self.write('S. Move down')
            self.write('W. Move up')
            self.write('D. Move right')

            self.window.wait_variable(self.input)

            choice = self.input.get()

            if choice.lower() == 'quit':
                self.window.quit()
            
            elif choice.lower() in ['a', 's', 'w', 'd']:
                return self.handle_player_movement(choice)

            else:
                raise ValueError

        except ValueError:
            self.write('Invalid value. Please type again')
            return self._display_movement_opt_menu()
    
    def handle_player_movement(self, movement_choice):
        if movement_choice == 'a':
            self.tilemap.move_player_left()
            
        elif movement_choice == 's':
            self.tilemap.move_player_down()

        elif movement_choice == 'w':
            self.tilemap.move_player_up()

        elif movement_choice == 'd':
            self.tilemap.move_player_right()

        if self.tilemap.encounter_mobs:
            import time
            self.write("Something blocked your way... \n")
            time.sleep(2)
            self.tilemap.start_battle()

        return self._display_movement_opt_menu()
