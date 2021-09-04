"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 23 April 2021
This file is for custom tkinter GUI
"""


from tkinter import Text, Label, Button, Entry, OptionMenu, StringVar, Scrollbar
from tkinter import ttk


class WindowStyle(object):
    def __init__(self, style_name, **kwargs):
        raise NotImplementedError()


class WindowText(object):
    def __init__(self, tk, **kwargs):
        self.tk = tk
        self.text = Text(self.tk, **kwargs)
        self.text.config(state='disable')

    def write(self, message: str):
        self.text.config(state="normal")
        self.text.insert('end', message)
        self.text.insert('end', "\n")
        self.tk.update()
        self.text.config(state="disable")
        self.text.see("end")

    def grid(self, **kwargs):
        return self.text.grid(**kwargs)


class WindowScrollbar(object):
    def __init__(self, tk, **kwargs):
        self.tk = tk
        self.scrollbar = Scrollbar(self.tk, **kwargs)
    
    def grid(self, **kwargs):
        return self.scrollbar.grid(**kwargs)
    
    def config(self, **kwargs):
        return self.scrollbar.config(**kwargs)


class WindowButton(object):
    def __init__(self, tk, **kwargs):
        self.tk = tk
        self.use_theme = kwargs.get('use_ttk', False)
        if self.use_theme:
            self.button = ttk.Button(self.tk, **kwargs)
        else:
            self.button = Button(self.tk, **kwargs)
            self.button.bind("<Enter>", self._on_hover)
            self.button.bind("<Leave>", self._on_leave)

    def grid(self, **kwargs):
        return self.button.grid(**kwargs)
    
    def pack(self, **kwargs):
        return self.button.pack(**kwargs)

    def place(self, **kwargs):
        return self.button.place(**kwargs)

    def _on_hover(self, event):
        self.button['background'] = 'grey'

    def _on_leave(self, event):
        self.button['background'] = 'SystemButtonFace'

    def destroy(self):
        return self.button.destroy()


class WindowFrame(object):
    def __init__(self, tk, **kwargs):
        self.tk = tk
        self.tk.style.configure("mybutton.TFrame", background="#E61E50")
        self.frame = ttk.Frame(self.tk, style="mybutton.TFrame", **kwargs)

    def add_button(self, **kwargs):
        return WindowButton(self.frame, **kwargs)

    def grid(self, **kwargs):
        return self.frame.grid(**kwargs)
    
    def destroy(self):
        return self.frame.destroy()


class WindowLabel(object):
    def __init__(self, tk, **kwargs):
        self.tk = tk
        self.use_theme = kwargs.get('use_ttk', False)
        if self.use_theme:
            self.label = ttk.Label(self.tk, **kwargs)
        else:
            self.label = Label(self.tk, **kwargs)

    def grid(self, **kwargs):
        return self.label.grid(**kwargs)

    def config(self, **kwargs):
        return self.label.config(**kwargs)

    def destroy(self):
        return self.label.destroy()


class WindowEntry(object):
    def __init__(self, tk, **kwargs):
        self.tk = tk
        self.use_theme = kwargs.get('use_ttk', False)
        if self.use_theme:
            self.entry = ttk.Entry(self.tk, **kwargs)
        else:
            self.entry = Entry(self.tk, **kwargs)

    def grid(self, **kwargs):
        return self.entry.grid(**kwargs)

    def get(self):
        return self.entry.get()

    def destroy(self):
        return self.entry.destroy()


class WindowOptions(object):
    def __init__(self, tk, *args, **kwargs):
        self.tk = tk
        self.use_theme = kwargs.get('use_ttk', False)
        self.option_listener = StringVar()
        self.option_listener.set(args[0])  # set to the first value of option

        if self.use_theme:
            self.option = ttk.OptionMenu(self.tk, self.option_listener, *args, **kwargs)
        else:
            self.option = OptionMenu(self.tk, self.option_listener, *args, **kwargs)

    def grid(self, **kwargs):
        return self.option.grid(**kwargs)

    def config(self, **kwargs):
        return self.option.config(**kwargs)

    def get(self):
        return self.option_listener.get()

    def destroy(self):
        return self.option.destroy()


class ChildConstructor(object):
    def __init__(self, tk):
        self.tk = tk

    def text(self, **kwargs):
        return WindowText(self.tk, **kwargs)

    def button(self, **kwargs):
        return WindowButton(self.tk, **kwargs)

    def frame(self, **kwargs):
        return WindowFrame(self.tk, **kwargs)

    def style(self, style_name, **kwargs):
        return WindowStyle(style_name, **kwargs)

    def label(self, **kwargs):
        return WindowLabel(self.tk, **kwargs)

    def input(self, **kwargs):
        return WindowEntry(self.tk, **kwargs)
    
    def options(self, *args, **kwargs):
        return WindowOptions(self.tk, *args, **kwargs)
    
    def scrollbar(self, **kwargs):
        return WindowScrollbar(self.tk, **kwargs)
