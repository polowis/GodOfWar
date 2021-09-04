"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 26 April 2021
This file is for game window GUI, all methods associated with window object or global methods
are defined in this class. Some global methods are save_file, open_file, display_popup_window()
Files read: none
Files write: user-selected-file.txt
"""

from tkinter import Tk, ttk, messagebox, filedialog
from .child_constructor import ChildConstructor
from config import SCENES
import sys


class Game(Tk):
    def __init__(self, **kwargs):
        super().__init__()

        self.config = kwargs
        self.screen_width = self.config.get("screen_width", 800)
        self.screen_height = self.config.get("screen_height", 500)
        self.number_of_columns = self.config.get("number_of_cols", 10)
        self.number_of_rows = self.config.get("number_of_rows", 10)
        self.grid_weight = self.config.get('grid_weight', 1)

        self.style = ttk.Style(self)
        self.add = ChildConstructor(self)
        self.active_scene = None
        self.storage = {}
        self.construct()

    def construct(self):
        self.geometry(f'{self.screen_width}x{self.screen_height}')
        for cols in range(self.number_of_columns):
            self.grid_columnconfigure(cols, weight=self.grid_weight)

        for rows in range(self.number_of_rows):
            self.grid_rowconfigure(rows, weight=self.grid_weight)
        
        self.configure(background=self.config.get("background", 'white'))

    def change_scene(self, window, scene_name):
        """Change scene"""
        if self.active_scene is not None:
            self.active_scene.destroy()

        main_scene = SCENES.get(scene_name)
        self.active_scene = main_scene(window)
        self.active_scene.run()

    def change_theme(self, theme_name='default'):
        self.style.theme_use(theme_name)

    def get_middle_column(self):
        return round((self.number_of_columns - 1) / 2)

    def get_middle_row(self):
        return round((self.number_of_rows - 1) / 2)

    def current_active_scene(self):
        return self.active_scene

    @property
    def user(self):
        """Return the Character Object of current user

        return None if no user found
        """
        return self.storage.get('authenticated_user', None)
    
    @user.setter
    def user(self, user_object):
        self.storage['authenticated_user'] = user_object
    
    @property
    def current_file_path(self):
        return self.storage.get('current_saved_file_path', None)
    
    @current_file_path.setter
    def current_file_path(self, path):
        self.storage['current_saved_file_path'] = path

    def quit(self):
        sys.exit(0)
    
    def display_popup_window(self, msg):
        """Show information in pop up window"""
        messagebox.showinfo('Information', msg)
    
    def save_file(self):
        """Prompt Save file window"""
        return filedialog.asksaveasfilename(defaultextension=".txt")
    
    def open_file(self):
        """Prompt Open file window"""
        return filedialog.askopenfilename()
        
    
