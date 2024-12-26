# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class UserManageView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.init_ui()

    def init_ui(self):
        # 创建工具栏框架
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(fill='x', padx=10, pady=5)

        # 搜索框
        search_frame = ttk.LabelFrame(toolbar_frame, text='搜索', padding=5)
        search_frame.pack(side='left', padx=5)

        # 添加搜索类型选择
        self.search_type = tk.StringVar(value='user_id')
        search_type_frame = ttk.Frame(search_frame)
        search_type_frame.pack(side='left', padx=5)

        ttk.Radiobutton(
            search_type_frame,
            text='ID',
            value='user_id',
            variable=self.search_type
        ).pack(side='left')

        # 搜索输入框
        self.search_var = tk.StringVar()
        ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=20
        ).pack(side='left', padx=5)

        ttk.Button(
            search_frame,
            text='搜索',
            command=self.search_users,
            width=10
        ).pack(side='left', padx=5)

        # 操作按钮
        btn_frame = ttk.Frame(toolbar_frame)
        btn_frame.pack(side='right', padx=5)

        ttk.Button(
            btn_frame,
            text='启用账号',
            command=lambda: self.toggle_user_status(1),
            width=15
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text='禁用账号',
            command=lambda: self.toggle_user_status(0),
            width=15
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text='重置密码',
            command=self.reset_password,
            width=15
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text='编辑信息',
            command=self.edit_user,
            width=15
        ).pack(side='left', padx=5)

        # 创建表格
        self.create_user_table()

        # 刷新按钮
        refresh_btn = ttk.Button(
            self,
            text='刷新列表',
            command=self.refresh_table,
            width=15
        )
        refresh_btn.pack(pady=10)

    def create_user_table(self):
        """创建用户表格"""
        # 创建表格框架
        table_frame = ttk.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 创建表格
        columns = (
            'user_id', 'username', 'role', 'real_name', 'phone',
            'email', 'created_at', 'last_login', 'status'
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )

        # 设置列标题
        column_headers = {
            'user_id': 'ID',
            'username': '用户名',
            'role': '角色',
            'real_name': '真实姓名',
            'phone': '联系电话',
            'email': '电子邮箱',
            'created_at': '创建时间',
            'last_login': '最后登录',
            'status': '状态'
        }

        # 设置列宽和标题
        for col in columns:
            self.tree.heading(col, text=column_headers[col])
            # 根据内容类型设置列宽
            if col in ['user_id', 'role', 'status']:
                width = 70
            elif col in ['username', 'real_name', 'phone']:
                width = 100
            elif col in ['created_at', 'last_login']:
                width = 150
            else:
                width = 200
            self.tree.column(col, width=width, anchor='center')

        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill='both', expand=True)

        # 加载数据
        self.refresh_table()

    def refresh_table(self):
        """刷新表格数据"""
        try:
            # 显示加载提示
            self.tree.pack_forget()
            loading_label = ttk.Label(
                self,
                text='正在加载数据...',
                font=('微软雅黑', 12)
            )
            loading_label.pack(expand=True)

            # 更新界面
            self.update()

            # 清空现有数据
            for item in self.tree.get_children():
                self.tree.delete(item)

            # 从数据库加载用户数据
            from models.user import UserManager
            users = UserManager.get_all_users()

            # 移除加载提示
            loading_label.destroy()
            self.tree.pack(fill='both', expand=True)

            # 显示数据
            for user in users:
                values = (
                    user['user_id'],
                    user['username'],
                    '管理员' if user['role'] == 'admin' else '普通用户',
                    user['real_name'],
                    user['phone'],
                    user['email'],
                    user['created_at'],
                    user['last_login'] or '从未登录',
                    '启用' if user['status'] == 1 else '禁用'
                )
                self.tree.insert('', 'end', values=values)

        except Exception as e:
            logger.error(f"刷新用户列表错误: {e}")
            messagebox.showerror('错误', f'加载用户列表失败：\n{str(e)}')

    def search_users(self):
        """搜索用户"""
        keyword = self.search_var.get().strip()
        if not keyword:
            self.refresh_table()
            return

        # 验证搜索条件
        if self.search_type.get() == 'user_id':
            try:
                user_id = int(keyword)
            except ValueError:
                messagebox.showwarning('错误', 'ID必须是数字！')
                return

        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 搜索显示结果
        from models.user import UserManager
        users = UserManager.search_users(keyword, self.search_type.get())
        for user in users:
            values = (
                user['user_id'],
                user['username'],
                '管理员' if user['role'] == 'admin' else '普通用户',
                user['real_name'],
                user['phone'],
                user['email'],
                user['created_at'],
                user['last_login'] or '从未登录',
                '启用' if user['status'] == 1 else '禁用'
            )
            self.tree.insert('', 'end', values=values)

    def toggle_user_status(self, status):
        """启用/禁用用户"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要操作的用户！')
            return

        user_id = self.tree.item(selected[0])['values'][0]
        action = '启用' if status == 1 else '禁用'

        if messagebox.askyesno('确认', f'确定要{action}选中的用户吗？'):
            from models.user import UserManager
            success, message = UserManager.update_user_status(user_id, status)
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)

    def reset_password(self):
        """重置用户密码"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要重置密码的用户！')
            return

        user_id = self.tree.item(selected[0])['values'][0]
        username = self.tree.item(selected[0])['values'][1]

        if messagebox.askyesno('确认', f'确定要重置用户 {username} 的密码吗？\n新密码将设置为：123456'):
            from models.user import UserManager
            success, message = UserManager.reset_password(user_id)
            if success:
                messagebox.showinfo('成功', message)
            else:
                messagebox.showerror('错误', message)

    def edit_user(self):
        """编辑用户信息"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要编辑的用户！')
            return

        # 获取选中的用户数据
        item = self.tree.item(selected[0])
        values = item['values']
        user_data = {
            'user_id': values[0],
            'username': values[1],
            'role': values[2],
            'real_name': values[3],
            'phone': values[4],
            'email': values[5]
        }

        def on_user_edit(new_data):
            from models.user import UserManager
            success, message = UserManager.update_user_info(user_data['user_id'], new_data)
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)

        from views.dialogs.user_edit import UserEditDialog
        UserEditDialog(self, user_data=user_data, callback=on_user_edit)
