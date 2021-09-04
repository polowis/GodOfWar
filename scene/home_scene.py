"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 26 April 2021
This file is for display GUI for starting scene and handle inputs
"""

from tkinter import StringVar
from scene.scene_interface import SceneInterface
from entity.constants import CHARACTER_JOB_OBJECTS


class HomeScene(SceneInterface):
    def __init__(self, window):
        self.window = window

    def run(self):
        self._display_welcome_message()
        self._display_name_input()
        self._display_job_menu()
        self._display_start_button()

    def _name_changed(self, *args):
        self.welcome_name_listener.set(f"WELCOME {self.name_input.get().upper()}")
        if len(self.name_input.get()) == 0:
            self.warning_name_blank_label.grid(column=self.window.get_middle_column(), row=3)
            self.name_label.label.grid_forget()
        else:
            self.warning_name_blank_label.label.grid_forget()
            self.name_label.grid(column=self.window.get_middle_column(), row=3)

    def _display_name_input(self):
        """Display UI for getting input name"""
        self.warning_name_blank_label = self.window.add.label(text="Your name cannot be missing", bg="#2C3E50", fg="red")
        self.warning_name_blank_label.grid(column=self.window.get_middle_column(), row=3)
        self.warning_name_blank_label.label.grid_forget()

        self.name_label = self.window.add.label(text="Enter your name", bg="#2C3E50", fg="white")
        self.name_label.grid(column=self.window.get_middle_column(), row=3)

        self.name_input = self.window.add.input(textvariable=self.name_listener)
        self.name_input.grid(column=self.window.get_middle_column() - 1, row=4, columnspan=3)

    def _display_job_menu(self):
        """Display UI for selecting job"""
        self.job_menu = self.window.add.options(*CHARACTER_JOB_OBJECTS.keys())
        self.job_menu.config(width=15)
        self.job_menu.grid(
            column=self.window.get_middle_column(),
            row=self.window.get_middle_row(),
        )

        self.job_menu_label = self.window.add.label(text="Select your job", bg="#2C3E50", fg="white")
        self.job_menu_label.grid(column=self.window.get_middle_column(), row=self.window.get_middle_row() - 1)

    def _display_start_button(self):
        self.start_button = self.window.add.button(text="Start", bg="#2C3E50", command=self.on_start)
        self.start_button.grid(
            column=self.window.get_middle_column(),
            row=self.window.get_middle_row() + 2,
            ipadx=25,
            ipady=7)

    def _display_welcome_message(self):
        self.name_listener = StringVar()
        self.name_listener.set("PLAYER")
        self.name_listener.trace("w", self._name_changed)

        self.welcome_name_listener = StringVar()
        self.welcome_name_listener.set("WELCOME PLAYER")

        self.welcome_label = self.window.add.label(
            textvariable=self.welcome_name_listener,
            font=("Courier", 30),
            fg="#03fc84",
            bg="#2C3E50"
        )
        self.welcome_label.grid(column=self.window.get_middle_column(), row=2)

    def on_start(self):
        """When start button is clicked"""
        if len(self.name_input.get()) == 0:
            return
        self.create_character(self.name_input.get(), self.job_menu.get())
        self.window.change_scene(self.window, 'main')

    def destroy(self):
        self.job_menu.destroy()
        self.job_menu_label.destroy()
        self.welcome_label.destroy()
        self.start_button.destroy()
        self.name_input.destroy()
        self.name_label.destroy()

    def create_character(self, character_name, job):
        self.window.storage['player_name'] = character_name
        self.window.storage['player_job'] = job