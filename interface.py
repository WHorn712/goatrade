
from tkinter import *

import Armazenamento
from Armazenamento import *



class Screen:
    """Operation of the software's main graphical screen"""
    def __init__(self):
        self.screen = Tk()
        self.screen.title("GOAT TRADER")
        self.screen.geometry("700x420")
        self.add_button_on_off()
        self.add_listBox()
        self.add_button_historic()
        self.add_info()
        self.add_list_news()
        self.screen.mainloop()

    def add_button_on_off(self):
        """Add Start/Stop Analysis of Operations button"""
        self.button = Button(self.screen, text="Iniciar", command=self.command_bt_start)
        self.button.grid(column=1, row=1, pady=10, ipadx=5, ipady=5)
        self.button.config(height=3, width=6)

    def add_listBox(self):
        """Add list of open operations"""
        self.listbox = Listbox(self.screen)
        self.listbox.grid(column=1, row=4, columnspan=40, pady=30, padx=10)
        self.listbox.config(height=15, width=50)

    def add_button_historic(self):
        """Add button to access operation history"""
        self.bt_history = Button(self.screen, text="Mostrar Histórico")
        self.bt_history.grid(column=1, row=4, padx=10, sticky='S')

    def add_info(self):
        """Add information (Name and balance) and button for trade settings"""
        self.frame_info = Frame(self.screen)
        self.frame_info.grid(column=50, row=1)
        self.info_name = Label(self.frame_info, text="WELLINGTON AUGUSTO HORN")
        self.info_name.grid(column=200,columnspan=100,row=1,sticky='NW', padx=150)
        self.info_balance = Label(self.frame_info, text="$ 1200,00")
        self.info_balance.grid(column=200, columnspan=100,row=2, sticky='NW', padx=150)
        self.bt_parameters = Button(self.frame_info, text="PARÂMETROS DE TRADE")
        self.bt_parameters.grid(column=200,columnspan=100,row=3,sticky='NW', padx=150)

    def add_list_news(self):
        """Add list of current news"""
        self.list_news = Listbox(self.screen)
        self.list_news.grid(column=30, row=4, columnspan=40, pady=30, padx=10)
        self.list_news.config(height=15, width=50)

    def command_bt_start(self):
        """Performs the software on/off function"""
        text_bt = self.button['text']
        if text_bt == "Iniciar":
            self.button.config(text="Desativar")
        elif text_bt == "Desativar":
            self.button.config(text="Iniciar")
        Storage.main_()










