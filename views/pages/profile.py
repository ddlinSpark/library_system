# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import re

logger = logging.getLogger(__name__)


class ProfileView(ttk.Frame):
    def __init__(self, master, current_user):
        super().__init__(master)
        self.current_user = current_user
        self.init_ui()

    def init_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self, padding="20 10 20 10")
        main_frame.pack(fill='both', expand=True)

        # 标题
        title_label = ttk.Label(
            main_frame,
            text='个人信息',
            font=('微软雅黑', 16, 'bold')
        )
        title_label.pack(pady=20)

        # 表单框架
        form_frame = ttk.LabelFrame(main_frame, text='基本信息', padding=15)
        form_frame.pack(fill='x', padx=50)

        # 用户名（只读）
        username_frame = ttk.Frame(form_frame)
        username_frame.pack(fill='x', pady=5)

        ttk.Label(
            username_frame,
            text='用户名:',
            font=('微软雅黑', 10)
        ).pack(side='left', padx=(0, 10))

        ttk.Label(
            username_frame,
            text=self.current_user['username'],
            font=('微软雅黑', 10)
        ).pack(side='left')

        # 角色（只读）
        role_frame = ttk.Frame(form_frame)
        role_frame.pack(fill='x', pady=5)

        ttk.Label(
            role_frame,
            text='用户角色:',
            font=('微软雅黑', 10)
        ).pack(side='left', padx=(0, 10))

        ttk.Label(
            role_frame,
            text='管理员' if self.current_user['role'] == 'admin' else '普通用户',
            font=('微软雅黑', 10)
        ).pack(side='left')

        # 真实姓名
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill='x', pady=5)

        ttk.Label(
            name_frame,
            text='真实姓名:  *',
            font=('微软雅黑', 10)
        ).pack(side='left', padx=(0, 10))

        self.name_var = tk.StringVar(value=self.current_user['real_name'] or '')
        self.name_entry = ttk.Entry(
            name_frame,
            textvariable=self.name_var,
            width=30
        )
        self.name_entry.pack(side='left')

        # 联系电话
        phone_frame = ttk.Frame(form_frame)
        phone_frame.pack(fill='x', pady=5)

        ttk.Label(
            phone_frame,
            text='联系电话:',
            font=('微软雅黑', 10)
        ).pack(side='left', padx=(0, 10))

        self.phone_var = tk.StringVar(value=self.current_user['phone'] or '')
        self.phone_entry = ttk.Entry(
            phone_frame,
            textvariable=self.phone_var,
            width=30
        )
        self.phone_entry.pack(side='left')

        # 电子邮箱
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill='x', pady=5)

        ttk.Label(
            email_frame,
            text='电子邮箱:',
            font=('微软雅黑', 10)
        ).pack(side='left', padx=(0, 10))

        self.email_var = tk.StringVar(value=self.current_user['email'] or '')
        self.email_entry = ttk.Entry(
            email_frame,
            textvariable=self.email_var,
            width=30
        )
        self.email_entry.pack(side='left')

        # 提示信息
        ttk.Label(
            form_frame,
            text='带 * 号的字段为必填项',
            font=('微软雅黑', 9),
            foreground='red'
        ).pack(pady=10)

        # 修改密码框架
        pwd_frame = ttk.LabelFrame(main_frame, text='修改密码', padding=15)
        pwd_frame.pack(fill='x', padx=50, pady=20)

        # 原密码
        old_pwd_frame = ttk.Frame(pwd_frame)
        old_pwd_frame.pack(fill='x', pady=5)

        ttk.Label(
            old_pwd_frame,
            text='原密码:',
            font=('微软雅黑', 10)
        ).pack(side='left', padx=(0, 10))

        self.old_pwd_var = tk.StringVar()
        self.old_pwd_entry = ttk.Entry(
            old_pwd_frame,
            textvariable=self.old_pwd_var,
            show='*',
            width=30
        )
        self.old_pwd_entry.pack(side='left')

        # 新密码
        new_pwd_frame = ttk.Frame(pwd_frame)
        new_pwd_frame.pack(fill='x', pady=5)

        ttk.Label(
            new_pwd_frame,
            text='新密码:',
            font=('微软雅黑', 10)
        ).pack(side='left', padx=(0, 10))

        self.new_pwd_var = tk.StringVar()
        self.new_pwd_entry = ttk.Entry(
            new_pwd_frame,
            textvariable=self.new_pwd_var,
            show='*',
            width=30
        )
        self.new_pwd_entry.pack(side='left')

        # 确认密码
        confirm_pwd_frame = ttk.Frame(pwd_frame)
        confirm_pwd_frame.pack(fill='x', pady=5)

        ttk.Label(
            confirm_pwd_frame,
            text='确认密码:',
            font=('微软雅黑', 10)
        ).pack(side='left', padx=(0, 10))

        self.confirm_pwd_var = tk.StringVar()
        self.confirm_pwd_entry = ttk.Entry(
            confirm_pwd_frame,
            textvariable=self.confirm_pwd_var,
            show='*',
            width=30
        )
        self.confirm_pwd_entry.pack(side='left')

        # 按钮框架
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)

        # 保存信息按钮
        save_info_btn = ttk.Button(
            btn_frame,
            text='保存信息',
            command=self.save_info,
            width=15
        )
        save_info_btn.pack(side='left', padx=10)

        # 修改密码按钮
        change_pwd_btn = ttk.Button(
            btn_frame,
            text='修改密码',
            command=self.change_password,
            width=15
        )
        change_pwd_btn.pack(side='left', padx=10)

    def validate_data(self):
        """验证表单数据"""
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

        return {
            'real_name': real_name,
            'phone': phone,
            'email': email
        }

    def save_info(self):
        """保存个人信息"""
        data = self.validate_data()
        if not data:
            return

        from models.user import UserManager
        success, message = UserManager.update_user_info(
            self.current_user['user_id'],
            data
        )

        if success:
            # 更新当前用户信息
            self.current_user.update(data)
            messagebox.showinfo('成功', message)
        else:
            messagebox.showerror('错误', message)

    def change_password(self):
        """修改密码"""
        # 获取并清理数据
        old_pwd = self.old_pwd_var.get().strip()
        new_pwd = self.new_pwd_var.get().strip()
        confirm_pwd = self.confirm_pwd_var.get().strip()

        # 验证数据
        if not all([old_pwd, new_pwd, confirm_pwd]):
            messagebox.showwarning('错误', '请填写所有密码字段！')
            return

        if new_pwd != confirm_pwd:
            messagebox.showwarning('错误', '两次输入的新密码不一致！')
            return

        if len(new_pwd) < 6:
            messagebox.showwarning('错误', '新密码长度不能少于6位！')
            return

        # 修改密码
        from models.user import UserManager
        success, message = UserManager.change_password(
            self.current_user['user_id'],
            old_pwd,
            new_pwd
        )

        if success:
            # 清空密码输入框
            self.old_pwd_var.set('')
            self.new_pwd_var.set('')
            self.confirm_pwd_var.set('')
            messagebox.showinfo('成功', message)
        else:
            messagebox.showerror('错误', message)
