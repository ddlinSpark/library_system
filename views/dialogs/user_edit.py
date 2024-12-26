# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import re

logger = logging.getLogger(__name__)


class UserEditDialog(tk.Toplevel):
    def __init__(self, parent, user_data=None, callback=None):
        super().__init__(parent)
        self.title("编辑用户信息")
        self.callback = callback
        self.user_data = user_data

        # 设置窗口属性
        self.geometry('500x400')
        self.resizable(False, False)
        self.transient(parent)  # 设置为父窗口的临时窗口
        self.grab_set()  # 模态窗口

        # 初始化界面
        self.init_ui()

        # 如果有用户数据，填充表单
        if user_data:
            self.fill_data()

    def init_ui(self):
        # 主框架
        main_frame = ttk.Frame(self, padding="20 10 20 10")
        main_frame.pack(fill='both', expand=True)

        # 表单框架
        form_frame = ttk.LabelFrame(main_frame, text='用户信息', padding=15)
        form_frame.pack(fill='x', padx=20)

        # 真实姓名
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill='x', pady=5)

        ttk.Label(
            name_frame,
            text='真实姓名:  *',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            name_frame,
            textvariable=self.name_var,
            width=40
        )
        self.name_entry.pack(fill='x', pady=(2, 0))

        # 联系电话
        phone_frame = ttk.Frame(form_frame)
        phone_frame.pack(fill='x', pady=5)

        ttk.Label(
            phone_frame,
            text='联系电话:',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(
            phone_frame,
            textvariable=self.phone_var,
            width=40
        )
        self.phone_entry.pack(fill='x', pady=(2, 0))

        # 电子邮箱
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill='x', pady=5)

        ttk.Label(
            email_frame,
            text='电子邮箱:',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            width=40
        )
        self.email_entry.pack(fill='x', pady=(2, 0))

        # 提示信息
        ttk.Label(
            main_frame,
            text='带 * 号的字段为必填项',
            font=('微软雅黑', 9),
            foreground='red'
        ).pack(pady=10)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        # 保存按钮
        save_btn = ttk.Button(
            button_frame,
            text='保存',
            command=self.save_user,
            width=15
        )
        save_btn.pack(side='left', padx=10)

        # 取消按钮
        cancel_btn = ttk.Button(
            button_frame,
            text='取消',
            command=self.destroy,
            width=15
        )
        cancel_btn.pack(side='left', padx=10)

    def fill_data(self):
        """填充用户数据"""
        self.name_var.set(self.user_data['real_name'] or '')
        self.phone_var.set(self.user_data['phone'] or '')
        self.email_var.set(self.user_data['email'] or '')

    def validate_data(self):
        """验证数据"""
        # 获取并清理数据
        real_name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        # 验证必填字段
        if not real_name:
            messagebox.showwarning('错误', '请填写真实姓名！')
            return None

        # 验证手机号格式
        if phone and (not phone.isdigit() or len(phone) != 11):
            messagebox.showwarning('错误', '手机号码格式不正确！')
            return None

        # 验证邮箱格式
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showwarning('错误', '邮箱格式不正确！')
            return None

        # 返回验证后的数据
        return {
            'real_name': real_name,
            'phone': phone,
            'email': email
        }

    def save_user(self):
        """保存用户信息"""
        data = self.validate_data()
        if data and self.callback:
            self.callback(data)
            self.destroy()
