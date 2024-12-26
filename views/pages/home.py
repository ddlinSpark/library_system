import tkinter as tk
from tkinter import ttk


class HomeView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.init_ui()

    def init_ui(self):
        welcome_label = ttk.Label(
            self,
            text='欢迎使用图书管理系统',
            font=('Helvetica', 16)
        )
        welcome_label.pack(expand=True)
