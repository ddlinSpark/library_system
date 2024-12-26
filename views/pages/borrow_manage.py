# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class BorrowManageView(ttk.Frame):
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
        self.search_type = tk.StringVar(value='record_id')
        search_type_frame = ttk.Frame(search_frame)
        search_type_frame.pack(side='left', padx=5)

        ttk.Radiobutton(
            search_type_frame,
            text='记录ID',
            value='record_id',
            variable=self.search_type
        ).pack(side='left')

        ttk.Radiobutton(
            search_type_frame,
            text='用户ID',
            value='user_id',
            variable=self.search_type
        ).pack(side='left')

        ttk.Radiobutton(
            search_type_frame,
            text='图书ID',
            value='book_id',
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
            command=self.search_records,
            width=10
        ).pack(side='left', padx=5)

        # 操作按钮
        btn_frame = ttk.Frame(toolbar_frame)
        btn_frame.pack(side='right', padx=5)

        ttk.Button(
            btn_frame,
            text='确认归还',
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
            'record_id', 'book_id', 'book_title', 'user_id', 'username',
            'borrow_date', 'due_date', 'return_date', 'status'
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
            'user_id': '用户ID',
            'username': '用户名',
            'borrow_date': '借出日期',
            'due_date': '应还日期',
            'return_date': '归还日期',
            'status': '状态'
        }

        # 设置列宽和标题
        for col in columns:
            self.tree.heading(col, text=column_headers[col])
            # 根据内容类型设置列宽
            if col in ['record_id', 'book_id', 'user_id', 'status']:
                width = 70
            elif col in ['username', 'book_title']:
                width = 150
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
            records = BorrowManager.get_all_records()

            # 移除加载提示
            loading_label.destroy()
            self.tree.pack(fill='both', expand=True)

            # 显示数据
            for record in records:
                values = (
                    record['record_id'],
                    record['book_id'],
                    record['book_title'],
                    record['user_id'],
                    record['username'],
                    record['borrow_date'],
                    record['due_date'],
                    record['return_date'] or '',
                    '已归还' if record['status'] == 'returned' else '借出'
                )
                self.tree.insert('', 'end', values=values)

        except Exception as e:
            logger.error(f"刷新借阅记录列表错误: {e}")
            messagebox.showerror('错误', f'加载借阅记录列表失败：\n{str(e)}')

    def search_records(self):
        """搜索借阅记录"""
        keyword = self.search_var.get().strip()
        if not keyword:
            self.refresh_table()
            return

        # 验证搜索条件
        try:
            keyword_id = int(keyword)
        except ValueError:
            messagebox.showwarning('错误', 'ID必须是数字！')
            return

        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 搜索并显示结果
        from models.borrow import BorrowManager
        records = BorrowManager.search_records(keyword, self.search_type.get())
        for record in records:
            values = (
                record['record_id'],
                record['book_id'],
                record['book_title'],
                record['user_id'],
                record['username'],
                record['borrow_date'],
                record['due_date'],
                record['return_date'] or '',
                '已归还' if record['status'] == 'returned' else '借出'
            )
            self.tree.insert('', 'end', values=values)

    def return_book(self):
        """确认图书归还"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要归还的记录！')
            return

        # 获取选中的记录数据
        item = self.tree.item(selected[0])
        values = item['values']

        # 检查是否已归还
        if values[8] == '已归还':
            messagebox.showwarning('提示', '该图书已经归还！')
            return

        if messagebox.askyesno('确认', '确定要将该图书标记为已归还吗？'):
            from models.borrow import BorrowManager
            success, message = BorrowManager.return_book(values[0])  # record_id
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)
