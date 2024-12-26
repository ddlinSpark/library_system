# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from models.user import UserManager
import logging
import re

logger = logging.getLogger(__name__)


class RegisterWindow(ttk.Frame):
    def __init__(self, master, on_register_complete=None):
        super().__init__(master)
        self.configure_styles()
        self.on_register_complete = on_register_complete
        self.init_ui()
        logger.info("注册窗口初始化完成")

    def configure_styles(self):
        """配置自定义样式"""
        style = ttk.Style()

        # 配置按钮样式
        style.configure(
            'Custom.TButton',
            font=('微软雅黑', 11),
            padding=8
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

    def init_ui(self):
        # 主框架
        main_frame = ttk.Frame(self, padding="40 20 40 20")
        main_frame.pack(fill='both', expand=True)

        # 标题
        title_label = ttk.Label(
            main_frame,
            text='用户注册',
            font=('华文中宋', 18, 'bold')
        )
        title_label.pack(pady=(0, 20))

        # 创建表单框架
        form_frame = ttk.LabelFrame(main_frame, text='请填写注册信息', padding=20)
        form_frame.pack(fill='x', padx=40)

        # 用户名输入
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill='x', pady=8)

        ttk.Label(
            username_frame,
            text='用户名:  *',
            font=('微软雅黑', 11)
        ).pack(side='top', anchor='w')

        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            username_frame,
            textvariable=self.username_var,
            width=40
        )
        self.username_entry.pack(fill='x', pady=(4, 0))
        ttk.Label(
            username_frame,
            text='用户名长度为3-20个字符',
            font=('微软雅黑', 9),
            foreground='gray'
        ).pack(side='top', anchor='w')

        # 密码输入
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill='x', pady=8)

        ttk.Label(
            password_frame,
            text='密码:  *',
            font=('微软雅黑', 11)
        ).pack(side='top', anchor='w')

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show='●',
            width=40
        )
        self.password_entry.pack(fill='x', pady=(4, 0))
        ttk.Label(
            password_frame,
            text='密码长度至少6位，包含字母和数字',
            font=('微软雅黑', 9),
            foreground='gray'
        ).pack(side='top', anchor='w')

        # 确认密码
        confirm_frame = ttk.Frame(form_frame)
        confirm_frame.pack(fill='x', pady=8)

        ttk.Label(
            confirm_frame,
            text='确认密码:  *',
            font=('微软雅黑', 11)
        ).pack(side='top', anchor='w')

        self.confirm_var = tk.StringVar()
        self.confirm_entry = ttk.Entry(
            confirm_frame,
            textvariable=self.confirm_var,
            show='●',
            width=40
        )
        self.confirm_entry.pack(fill='x', pady=(4, 0))

        # 真实姓名
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill='x', pady=8)

        ttk.Label(
            name_frame,
            text='真实姓名:  *',
            font=('微软雅黑', 11)
        ).pack(side='top', anchor='w')

        self.real_name_var = tk.StringVar()
        self.real_name_entry = ttk.Entry(
            name_frame,
            textvariable=self.real_name_var,
            width=40
        )
        self.real_name_entry.pack(fill='x', pady=(4, 0))

        # 手机号码
        phone_frame = ttk.Frame(form_frame)
        phone_frame.pack(fill='x', pady=8)

        ttk.Label(
            phone_frame,
            text='手机号码:',
            font=('微软雅黑', 11)
        ).pack(side='top', anchor='w')

        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(
            phone_frame,
            textvariable=self.phone_var,
            width=40
        )
        self.phone_entry.pack(fill='x', pady=(4, 0))
        ttk.Label(
            phone_frame,
            text='请输入11位手机号码',
            font=('微软雅黑', 9),
            foreground='gray'
        ).pack(side='top', anchor='w')

        # 电子邮箱
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill='x', pady=8)

        ttk.Label(
            email_frame,
            text='电子邮箱:',
            font=('微软雅黑', 11)
        ).pack(side='top', anchor='w')

        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            width=40
        )
        self.email_entry.pack(fill='x', pady=(4, 0))

        # 提示信息
        ttk.Label(
            main_frame,
            text='带 * 号的字段为必填项',
            font=('微软雅黑', 9),
            foreground='red'
        ).pack(pady=10)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=30)

        # 注册按钮
        register_btn = ttk.Button(
            button_frame,
            text='注册',
            command=self.do_register,
            style='Custom.TButton',
            width=20
        )
        register_btn.pack(side='left', padx=15)

        # 返回按钮
        back_btn = ttk.Button(
            button_frame,
            text='返回登录',
            command=self.back_to_login,
            style='Custom.TButton',
            width=20
        )
        back_btn.pack(side='left', padx=15)

        # 版权信息
        ttk.Label(
            main_frame,
            text='© 2024 林华东、黄鸿乐、韦嘉豪  All Rights Reserved',
            font=('微软雅黑', 9)
        ).pack(side='bottom', pady=10)

        # 绑定回车键
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.confirm_entry.focus())
        self.confirm_entry.bind('<Return>', lambda e: self.real_name_entry.focus())
        self.real_name_entry.bind('<Return>', lambda e: self.phone_entry.focus())
        self.phone_entry.bind('<Return>', lambda e: self.email_entry.focus())
        self.email_entry.bind('<Return>', lambda e: self.do_register())

        # 设置初始焦点
        self.username_entry.focus()

    def validate_register(self):
        """验证注册信息"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        confirm = self.confirm_var.get().strip()
        real_name = self.real_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        # 验证必填字段
        if not all([username, password, confirm, real_name]):
            messagebox.showwarning('错误', '请填写所有必填字段！')
            return False

        # 验证用户名长度
        if not (3 <= len(username) <= 20):
            messagebox.showwarning('错误', '用户名长度必须在3-20个字符之间！')
            return False

        # 验证密码长度和复杂度
        if len(password) < 6:
            messagebox.showwarning('错误', '密码长度不能少于6位！')
            return False

        if not (re.search(r'[A-Za-z]', password) and re.search(r'[0-9]', password)):
            messagebox.showwarning('错误', '密码必须包含字母和数字！')
            return False

        # 验证两次密码是否一致
        if password != confirm:
            messagebox.showwarning('错误', '两次输入的密码不一致！')
            return False

        # 验证手机号格式
        if phone and (not phone.isdigit() or len(phone) != 11):
            messagebox.showwarning('错误', '手机号码格式不正确！')
            return False

        # 验证邮箱格式
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showwarning('错误', '邮箱格式不正确！')
            return False

        return True

    def do_register(self):
        """执行注册"""
        if not self.validate_register():
            return

        success, message = UserManager.register_user(
            self.username_var.get().strip(),
            self.password_var.get().strip(),
            self.real_name_var.get().strip(),
            self.phone_var.get().strip(),
            self.email_var.get().strip()
        )

        if success:
            messagebox.showinfo('成功', message)
            if self.on_register_complete:
                self.on_register_complete()
        else:
            messagebox.showerror('错误', message)

    def back_to_login(self):
        """返回登录页面"""
        if self.on_register_complete:
            self.on_register_complete()
