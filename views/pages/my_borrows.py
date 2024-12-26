# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class MyBorrowsView(ttk.Frame):
    def __init__(self, master, current_user):
        super().__init__(master)
        self.current_user = current_user
        self.init_ui()

    def init_ui(self):
        # 创建工具栏框架
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(fill='x', padx=10, pady=5)

        # 状态筛选
        filter_frame = ttk.LabelFrame(toolbar_frame, text='状态筛选', padding=5)
        filter_frame.pack(side='left', padx=5)

        self.status_var = tk.StringVar(value='all')
        ttk.Radiobutton(
            filter_frame,
            text='全部',
            value='all',
            variable=self.status_var,
            command=self.refresh_table
        ).pack(side='left')

        ttk.Radiobutton(
            filter_frame,
            text='借阅中',
            value='borrowed',
            variable=self.status_var,
            command=self.refresh_table
        ).pack(side='left')

        ttk.Radiobutton(
            filter_frame,
            text='已归还',
            value='returned',
            variable=self.status_var,
            command=self.refresh_table
        ).pack(side='left')

        # 操作按钮
        btn_frame = ttk.Frame(toolbar_frame)
        btn_frame.pack(side='right', padx=5)

        ttk.Button(
            btn_frame,
            text='续借图书',
            command=self.renew_book,
            width=15
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text='归还图书',
            command=self.return_book,
            width=15
        ).pack(side='left', padx=5)

        # 创建表格
        self.create_borrow_table()

        # 刷新按钮
        refresh_btn = ttk.Button(
            self,
            text='刷新列表',
            command=self.refresh_table,
            width=15
        )
        refresh_btn.pack(pady=10)

    def create_borrow_table(self):
        """创建借阅记录表格"""
        # 创建表格框架
        table_frame = ttk.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 创建表格
        columns = (
            'record_id', 'book_id', 'book_title', 'borrow_date',
            'due_date', 'return_date', 'status'
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )

        # 设置列标题
        column_headers = {
            'record_id': '记录ID',
            'book_id': '图书ID',
            'book_title': '图书名称',
            'borrow_date': '借出日期',
            'due_date': '应还日期',
            'return_date': '归还日期',
            'status': '用户状态'
        }

        # 设置列宽和标题
        for col in columns:
            self.tree.heading(col, text=column_headers[col])
            # 根据内容类型设置列宽
            if col in ['record_id', 'book_id', 'status']:
                width = 70
            elif col == 'book_title':
                width = 200
            else:
                width = 100
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

            # 从数据库加载借阅记录
            from models.borrow import BorrowManager
            records = BorrowManager.get_user_records(
                self.current_user['user_id'],
                self.status_var.get()
            )

            # 移除加载提示
            loading_label.destroy()
            self.tree.pack(fill='both', expand=True)

            # 显示数据
            for record in records:
                values = (
                    record['record_id'],
                    record['book_id'],
                    record['book_title'],
                    record['borrow_date'],
                    record['due_date'],
                    record['return_date'] or '',
                    '已归还' if record['status'] == 'returned' else '借出'
                )
                self.tree.insert('', 'end', values=values)

        except Exception as e:
            logger.error(f"刷新借阅记录列表错误: {e}")
            messagebox.showerror('错误', f'加载借阅记录列表失败：\n{str(e)}')

    def return_book(self):
        """归还图书"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要归还的记录！')
            return

        # 获取选中的记录数据
        item = self.tree.item(selected[0])
        values = item['values']

        # 检查是否已归还
        if values[6] == '已归还':
            messagebox.showwarning('提示', '该图书已经归还！')
            return

        if messagebox.askyesno('确认', f'确定要归还《{values[2]}》吗？'):
            from models.borrow import BorrowManager
            success, message = BorrowManager.return_book(values[0])  # record_id
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)

    def renew_book(self):
        """续借图书"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要续借的记录！')
            return

        # 获取选中的记录数据
        item = self.tree.item(selected[0])
        values = item['values']

        # 检查是否已归还
        if values[6] == '已归还':
            messagebox.showwarning('提示', '该图书已经归还，无法续借！')
            return

        if messagebox.askyesno('确认', f'确定要续借《{values[2]}》吗？\n续借后可以继续借阅30天。'):
            from models.borrow import BorrowManager
            success, message = BorrowManager.renew_book(values[0])  # record_id
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)
