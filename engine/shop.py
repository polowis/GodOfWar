"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 23 April 2021
This file is for shop interface, mostly include UI. All calculations are kept to be simple
Files read: item.json
"""

from tkinter import Toplevel, Label, Radiobutton, IntVar, Canvas, Scrollbar, Button, StringVar

SHOP_ITEMS = {
    'revita(L)': 10,
    'revita(S)': 5,
    'revita(M)': 7,
    'revita(XL)': 20,
    'revita(XS)': 2,
}


class Shop(object):
    """
    The shop UI. It includes UI and methods that can be used within the shop. \n
    Parameters required:

    :param Player: A Character Entity that enters the shop \n
    :param Scene: The current Scene object in order to create top level window

    """
    def __init__(self, player, scene):
        self.player = player
        self.scene = scene
        self.total_coin = 0
        self.item_price_list = list(SHOP_ITEMS.values())
    
    def enter(self):
        """Enter the shop"""
        self._display_UI()
    
    def _display_UI(self):
        """Display GUI for the shop."""
        self.shop_root_window = Toplevel(self.scene.window, background='#2C3E50')
        self.shop_root_window.title('Shop')
        self.shop_root_window.geometry('600x300')

        shop_label = Label(self.shop_root_window,
                           text='What would you like to do?',
                           bg="#2C3E50", fg="white")
        shop_label.pack(fill='x')

        self._display_buy_sell_menu_opt()

        self.shop_window = Canvas(self.shop_root_window,
                                  bg="#2C3E50", width=600,
                                  height=300
                                  )
        self.shop_window.pack(fill="both", expand=True)

        for cols in range(10):
            self.shop_window.grid_columnconfigure(cols, weight=1)
        for rows in range(10):
            self.shop_window.grid_rowconfigure(rows, weight=1)
    
    def _display_buy_sell_menu_opt(self):
        """
        Display the radio button choices for selecting method to use in shop.
        Available methods are buy and sell.
        """
        shop_function_listener = IntVar()

        def listen_shop_choice():
            choice = shop_function_listener.get()
            if choice == 1:
                self._display_buy_menu(self.shop_window)
            elif choice == 2:
                self._display_sell_menu(self.shop_window)

        buy_option = Radiobutton(self.shop_root_window, text='Buy',
                                 variable=shop_function_listener,
                                 value=1,
                                 bg="#2C3E50",
                                 fg="white",
                                 command=listen_shop_choice
                                 )
        buy_option.pack(side='left')
        sell_radio_option = Radiobutton(self.shop_root_window,
                                        text='Sell',
                                        variable=shop_function_listener,
                                        value=2,
                                        bg="#2C3E50",
                                        fg="white",
                                        command=listen_shop_choice
                                        )
        sell_radio_option.pack(side='left')
    
    def _display_total_price(self):
        """
        Display total price label \n
        It will increase every time the quantity of selected items increase
        """
        self.total_listener = StringVar()
        self.total_listener.set('Total: {}'.format(self.total_coin))
        total_price_label = Label(self.shop_root_window, textvariable=self.total_listener, bg="#2C3E50", fg="white")
        total_price_label.place(x=5, y=200)
    
    def _display_sell_menu(self, window):
        Label(window, text="Not implemented yet", bg="#2C3E50", fg="white")
        
    def _display_buy_menu(self, window):
        """
        Show the buy menu table
        
        :param window: Canvas object.
        """
        self._display_total_price()

        def buy_item(index, item_name):
            number_of_items = quantity_vars[index].get()
            total_coins = number_of_items * self.item_price_list[index]
            if self.player.coin < total_coins:
                self.total_listener.set("You don't have enough coins")
            else:
                self.player.inventory.add(item_name, number_of_items)
                self.player.coin -= total_coins
                self.total_coin -= total_coins
                quantity_vars[index].set(0)
                self.total_listener.set("Total: {}".format(self.total_coin))
            
        row = 20
        quantity_vars = []
        for item in SHOP_ITEMS.items():
            item_index = list(SHOP_ITEMS.keys()).index(item[0])
            item_label = Label(window,
                               text=item[0],
                               bg="#2C3E50",
                               fg="white")
            
            window.create_window(20, row, window=item_label, anchor='nw')

            item_price = Label(window,
                               text=f'${item[1]}',
                               bg="#2C3E50",
                               fg="white")
            window.create_window(100, row, window=item_price, anchor='nw')

            item_quantity = IntVar()
            item_quantity.set(0)
            quantity_vars.append(item_quantity)

            item_quantity_label = Label(window,
                                        textvariable=quantity_vars[item_index],
                                        bg="#2C3E50",
                                        fg="white")
            
            window.create_window(170, row, window=item_quantity_label, anchor='nw')

            def increase_quantity(index):
                quantity_vars[index].set(quantity_vars[index].get() + 1)
                self.total_coin += self.item_price_list[index]
                self.total_listener.set("Total: {}".format(self.total_coin))
            
            def decrease_quantity(index):
                if quantity_vars[index].get() == 0:
                    quantity_vars[index].set(0)
                else:
                    quantity_vars[index].set(quantity_vars[index].get() - 1)
                    self.total_coin -= self.item_price_list[index]
                    self.total_listener.set("Total: {}".format(self.total_coin))

            item_increase_quantity_button = Button(window,
                                                   text='+',
                                                   bg="#2C3E50",
                                                   command=lambda x=item_index: increase_quantity(x))
            window.create_window(200, row, window=item_increase_quantity_button, anchor='nw')
            item_decrease_quantity_button = Button(window,
                                                   text='-',
                                                   bg="#2C3E50",
                                                   command=lambda x=item_index: decrease_quantity(x))
            window.create_window(230, row, window=item_decrease_quantity_button, anchor='nw')

            item_buy_button = Button(window, text='Buy', bg="#2C3E50", command=lambda x=item_index, y=item[0]: buy_item(x, y))
            window.create_window(260, row, window=item_buy_button, anchor='nw')
            row += 60
        
        scrollbar = Scrollbar(window, orient='vertical', command=window.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        window.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, row))

