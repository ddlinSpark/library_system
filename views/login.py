# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import UserManager
import logging

from views.register import RegisterWindow

logger = logging.getLogger(__name__)


class LoginWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure_styles()  # 确保在init_ui之前配置样式
        self.init_ui()
        logger.info("登录窗口初始化完成")

    def init_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True)

        # 创建登录框架并添加边框效果
        login_frame = ttk.LabelFrame(main_frame, text='')
        login_frame.pack(padx=80, pady=40, ipadx=40, ipady=20)

        # 设置标题
        title_frame = ttk.Frame(login_frame)
        title_frame.pack(fill='x', pady=(0, 20))

        title_label = ttk.Label(
            title_frame,
            text='图书管理系统',
            font=('华文中宋', 24, 'bold')
        )
        title_label.pack(pady=10)

        subtitle_label = ttk.Label(
            title_frame,
            text='Library Management System',
            font=('Times New Roman', 12)
        )
        subtitle_label.pack()

        # 分隔线
        separator = ttk.Separator(login_frame, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=10)

        # 用户名输入框架
        username_frame = ttk.Frame(login_frame)
        username_frame.pack(fill='x', padx=30, pady=8)

        username_label = ttk.Label(
            username_frame,
            text='用户名:',
            font=('微软雅黑', 11)
        )
        username_label.pack(side='top', anchor='w')

        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            username_frame,
            textvariable=self.username_var,
            width=40
        )
        self.username_entry.pack(fill='x', pady=(4, 0))

        # 密码输入框架
        password_frame = ttk.Frame(login_frame)
        password_frame.pack(fill='x', padx=30, pady=8)

        password_label = ttk.Label(
            password_frame,
            text='密码:',
            font=('微软雅黑', 11)
        )
        password_label.pack(side='top', anchor='w')

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show='●',
            width=40
        )
        self.password_entry.pack(fill='x', pady=(4, 0))

        # 角色选择框架
        role_frame = ttk.LabelFrame(login_frame, text='登录角色', padding=10)
        role_frame.pack(pady=15, padx=30, fill='x')

        # 角色选择单选按钮
        self.role_var = tk.StringVar(value='user')

        role_btn_frame = ttk.Frame(role_frame)
        role_btn_frame.pack(pady=8)

        ttk.Radiobutton(
            role_btn_frame,
            text='用户登录',
            value='user',
            variable=self.role_var,
            style='Custom.TRadiobutton'
        ).pack(side='left', padx=40)

        ttk.Radiobutton(
            role_btn_frame,
            text='管理员登录',
            value='admin',
            variable=self.role_var,
            style='Custom.TRadiobutton'
        ).pack(side='left', padx=40)

        # 按钮框架
        button_frame = ttk.Frame(login_frame)
        button_frame.pack(pady=30)

        # 登录按钮
        login_btn = ttk.Button(
            button_frame,
            text='登录',
            command=self.handle_login,
            style='Custom.TButton',
            width=20
        )
        login_btn.pack(side='left', padx=15)

        # 注册按钮
        register_btn = ttk.Button(
            button_frame,
            text='注册',
            command=self.show_register,
            style='Custom.TButton',
            width=20
        )
        register_btn.pack(side='left', padx=15)

        # 版权信息
        ttk.Label(
            main_frame,
            text='© 2024 林华东、黄鸿乐、韦嘉豪  All Rights Reserved',
            font=('微软雅黑', 9)
        ).pack(side='bottom', pady=10)

        # 配置样式
        self.configure_styles()

        # 绑定回车键
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

        # 默认焦点
        self.username_entry.focus()

    def configure_styles(self):
        """配置自定义样式"""
        style = ttk.Style()

        # 配置按钮样式
        style.configure(
            'Custom.TButton',
            font=('微软雅黑', 11),
            padding=8
        )

        # 配置单选按钮样式
        style.configure(
            'Custom.TRadiobutton',
            font=('微软雅黑', 11)
        )

        # 配置标签样式
        style.configure(
            'TLabel',
            font=('微软雅黑', 11)
        )

        # 配置输入框样式
        style.configure(
            'TEntry',
            padding=8
        )

        # 配置LabelFrame样式
        style.configure(
            'TLabelFrame',
            font=('微软雅黑', 10)
        )

    def show_register(self):
        """显示注册页面"""
        self.pack_forget()  # 隐藏登录页面
        from views.register import RegisterWindow  # 动态导入避免循环引用
        register_window = RegisterWindow(self.master, self.on_register_complete)
        register_window.pack(fill='both', expand=True)

    def on_register_complete(self):
        """注册完成后的回调"""
        for widget in self.master.winfo_children():
            if isinstance(widget, RegisterWindow):
                widget.destroy()
        self.pack(fill='both', expand=True)  # 显示登录页面

    def handle_login(self):
        try:
            username = self.username_var.get().strip()
            password = self.password_var.get().strip()
            role = self.role_var.get()  # 获取选择的角色

            if not username or not password:
                messagebox.showwarning('错误', '用户名和密码不能为空！')
                return

            user = UserManager.verify_user(username, password, role)  # 传递角色参数
            logger.info(f"登录验证结果: {user}")

            if user:
                if user['status'] != 1:
                    messagebox.showwarning('错误', '该账号已被禁用！')
                    return

                if user['role'] != role:  # 验证角色是否匹配
                    messagebox.showwarning('错误', '登录角色与账号不匹配！')
                    return

                messagebox.showinfo('成功', f"欢迎回来，{user['real_name'] or user['username']}！")
                if hasattr(self, 'on_login_success'):
                    self.on_login_success(user)
            else:
                messagebox.showwarning('错误', '用户名或密码错误！')

        except Exception as e:
            logger.error(f"登录过程发生错误: {e}")
            messagebox.showerror('错误', f'登录过程发生错误: {str(e)}')
