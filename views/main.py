# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from views.login import LoginWindow
from views.pages.home import HomeView
from views.pages.book_manage import BookManageView
from views.pages.about import AboutView
from models.database import test_connection
import logging

logger = logging.getLogger(__name__)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # 测试数据库连接
        if not test_connection():
            messagebox.showerror(
                '错误',
                '无法连接到数据库，程序将退出。\n请检查数据库配置和服务状态。'
            )
            self.destroy()
            return

        self.title('图书管理系统')
        self.geometry('1024x768')

        # 设置窗口最小尺寸
        self.minsize(1024, 768)

        # 将窗口居中显示
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1024) // 2
        y = (screen_height - 768) // 2
        self.geometry(f'1024x768+{x}+{y}')

        # 保存当前用户信息
        self.current_user = None

        # 创建登录窗口
        self.login_frame = LoginWindow(self)
        self.login_frame.pack(fill='both', expand=True)

        # 创建主界面
        self.main_frame = tk.Frame(self)

        # 创建导航栏
        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(fill='x', padx=5, pady=5)

        # 创建内容区域
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill='both', expand=True)

        # 创建各个页面
        self.home_view = HomeView(self.content_frame)
        self.book_manage_view = BookManageView(self.content_frame)
        self.about_view = AboutView(self.content_frame)

        # 绑定登录成功事件
        self.login_frame.on_login_success = self.on_login_success

        # 设置窗口图标（果有的话）
        try:
            self.iconbitmap('assets/icon.ico')
        except:
            pass

    def create_nav_buttons(self):
        """根据用户角色创建导航按钮"""
        # 清除现有按钮
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        # 基本按钮（所有用户都可见）
        self.home_btn = ttk.Button(
            self.nav_frame,
            text='首页'.encode('utf-8').decode('utf-8'),
            command=lambda: self.show_frame(self.home_view)
        )
        self.home_btn.pack(side='left', padx=5)

        # 用户功能按钮
        if self.current_user['role'] == 'user':
            ttk.Button(
                self.nav_frame,
                text='我的借阅'.encode('utf-8').decode('utf-8'),
                command=self.show_my_borrows
            ).pack(side='left', padx=5)

            ttk.Button(
                self.nav_frame,
                text='图书查询'.encode('utf-8').decode('utf-8'),
                command=self.show_book_search
            ).pack(side='left', padx=5)

        # 管理员功能按钮
        elif self.current_user['role'] == 'admin':
            ttk.Button(
                self.nav_frame,
                text='图书管理'.encode('utf-8').decode('utf-8'),
                command=lambda: self.show_frame(self.book_manage_view)
            ).pack(side='left', padx=5)

            ttk.Button(
                self.nav_frame,
                text='用户管理'.encode('utf-8').decode('utf-8'),
                command=self.show_user_manage
            ).pack(side='left', padx=5)

            ttk.Button(
                self.nav_frame,
                text='借阅管理'.encode('utf-8').decode('utf-8'),
                command=self.show_borrow_manage
            ).pack(side='left', padx=5)

        # 关于按钮（所有用户都可见）
        ttk.Button(
            self.nav_frame,
            text='关于'.encode('utf-8').decode('utf-8'),
            command=lambda: self.show_frame(self.about_view)
        ).pack(side='left', padx=5)

        # 用户信息和退出按钮（右侧）
        ttk.Button(
            self.nav_frame,
            text='个人中心'.encode('utf-8').decode('utf-8'),
            command=self.show_profile
        ).pack(side='right', padx=5)

        ttk.Button(
            self.nav_frame,
            text='退出登录'.encode('utf-8').decode('utf-8'),
            command=self.logout
        ).pack(side='right', padx=5)

        ttk.Label(
            self.nav_frame,
            text=f'当前用户: {self.current_user["real_name"] or self.current_user["username"]}'.encode('utf-8').decode(
                'utf-8')
        ).pack(side='right', padx=10)

    def show_frame(self, frame):
        """显示指定页面"""
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
        frame.pack(fill='both', expand=True)

    def on_login_success(self, user):
        """登录成功后的处理"""
        self.current_user = user
        self.login_frame.pack_forget()
        self.main_frame.pack(fill='both', expand=True)
        self.create_nav_buttons()  # 根据用户角色创建导航按钮
        self.show_frame(self.home_view)

    def logout(self):
        """退出登录"""
        self.current_user = None
        self.main_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)
        # 清除登录框中的用户名和密码
        self.login_frame.username_var.set('')
        self.login_frame.password_var.set('')

    # 以下方法将在后续实现
    def show_my_borrows(self):
        """显示我的借阅页面"""
        from views.pages.my_borrows import MyBorrowsView
        if not hasattr(self, 'my_borrows_view'):
            self.my_borrows_view = MyBorrowsView(self.content_frame, self.current_user)
        self.show_frame(self.my_borrows_view)

    def show_book_search(self):
        """显示图书查询页面"""
        from views.pages.book_search import BookSearchView
        if not hasattr(self, 'book_search_view'):
            self.book_search_view = BookSearchView(self.content_frame, self.current_user)
        self.show_frame(self.book_search_view)

    def show_user_manage(self):
        """显示用户管理页面"""
        from views.pages.user_manage import UserManageView
        if not hasattr(self, 'user_manage_view'):
            self.user_manage_view = UserManageView(self.content_frame)
        self.show_frame(self.user_manage_view)

    def show_borrow_manage(self):
        """显示借阅管理页面"""
        from views.pages.borrow_manage import BorrowManageView
        if not hasattr(self, 'borrow_manage_view'):
            self.borrow_manage_view = BorrowManageView(self.content_frame)
        self.show_frame(self.borrow_manage_view)

    def show_profile(self):
        """显示个人中心页面"""
        try:
            from views.pages.profile import ProfileView
            if not hasattr(self, 'profile_view'):
                logger.info(f"创建个人中心页面，用户信息: {self.current_user}")
                self.profile_view = ProfileView(self.content_frame, self.current_user)
            self.show_frame(self.profile_view)
        except Exception as e:
            logger.error(f"显示个人中中心页面错误: {e}")
            messagebox.showerror('错误', f'无法显示个人中心页面：\n{str(e)}')
