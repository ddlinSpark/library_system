from tkinter import ttk


class AboutView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.init_ui()

    def init_ui(self):
        ttk.Label(
            self,
            text='图书管理系统 v1.0',
            font=('Helvetica', 16)
        ).pack(pady=10)

        ttk.Label(
            self,
            text='版本号：1.0.0'
        ).pack(pady=5)

        ttk.Label(
            self,
            text='开发团队：林华东、黄鸿乐、韦嘉豪',
            font=('SimSun', 12)
        ).pack(pady=5)
