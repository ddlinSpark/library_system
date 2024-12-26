# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class BookSearchView(ttk.Frame):
    def __init__(self, master, current_user):
        super().__init__(master)
        self.current_user = current_user
        self.init_ui()

    def init_ui(self):
        # 创建工具栏框架
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.pack(fill='x', padx=10, pady=5)

        # 搜索框
        search_frame = ttk.LabelFrame(toolbar_frame, text='搜索', padding=5)
        search_frame.pack(side='left', padx=5)

        # 搜索类型选择
        self.search_type = tk.StringVar(value='title')
        ttk.Radiobutton(
            search_frame,
            text='书名',
            value='title',
            variable=self.search_type
        ).pack(side='left')

        ttk.Radiobutton(
            search_frame,
            text='作者',
            value='author',
            variable=self.search_type
        ).pack(side='left')

        ttk.Radiobutton(
            search_frame,
            text='ISBN',
            value='isbn',
            variable=self.search_type
        ).pack(side='left')

        # 搜索输入框
        self.search_var = tk.StringVar()
        ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30
        ).pack(side='left', padx=5)

        ttk.Button(
            search_frame,
            text='搜索',
            command=self.search_books,
            width=10
        ).pack(side='left', padx=5)

        # 操作按钮
        btn_frame = ttk.Frame(toolbar_frame)
        btn_frame.pack(side='right', padx=5)

        ttk.Button(
            btn_frame,
            text='借阅图书',
            command=self.borrow_book,
            width=15
        ).pack(side='left', padx=5)

        # 创建表格
        self.create_book_table()

        # 刷新按钮
        refresh_btn = ttk.Button(
            self,
            text='刷新列表',
            command=self.refresh_table,
            width=15
        )
        refresh_btn.pack(pady=10)

    def create_book_table(self):
        """创建图书表格"""
        # 创建表格框架
        table_frame = ttk.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 创建表格
        columns = (
            'book_id', 'isbn', 'title', 'author', 'publisher',
            'publish_date', 'category', 'location', 'price',
            'total_copies', 'available_copies', 'status'
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )

        # 设置列标题
        column_headers = {
            'book_id': 'ID',
            'isbn': 'ISBN',
            'title': '书名',
            'author': '作者',
            'publisher': '出版社',
            'publish_date': '出版日期',
            'category': '分类',
            'location': '馆藏位置',
            'price': '价格',
            'total_copies': '总复本数',
            'available_copies': '可借复本数',
            'status': '状态'
        }

        # 设置列宽和标题
        for col in columns:
            self.tree.heading(col, text=column_headers[col])
            # 根据内容类型设置列宽
            if col in ['book_id', 'status']:
                width = 50
            elif col in ['isbn', 'publish_date', 'category', 'location']:
                width = 100
            elif col in ['title', 'author', 'publisher']:
                width = 150
            else:
                width = 80
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

            # 从数据库加载图书数据
            from models.book import BookManager
            books = BookManager.get_all_books()

            # 移除加载提示
            loading_label.destroy()
            self.tree.pack(fill='both', expand=True)

            # 显示数据
            for book in books:
                values = (
                    book['book_id'],
                    book['isbn'],
                    book['title'],
                    book['author'],
                    book['publisher'],
                    book['publish_date'],
                    book['category'],
                    book['location'],
                    book['price'],
                    book['total_copies'],
                    book['available_copies'],
                    book['status']
                )
                self.tree.insert('', 'end', values=values)

        except Exception as e:
            logger.error(f"刷新图书列表错误: {e}")
            messagebox.showerror('错误', f'加载图书列表失败：\n{str(e)}')

    def search_books(self):
        """搜索图书"""
        keyword = self.search_var.get().strip()
        if not keyword:
            self.refresh_table()
            return

        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 搜索并显示结果
        from models.book import BookManager
        books = BookManager.search_books_by_keyword(keyword, self.search_type.get())
        for book in books:
            values = (
                book['book_id'],
                book['isbn'],
                book['title'],
                book['author'],
                book['publisher'],
                book['publish_date'],
                book['category'],
                book['location'],
                book['price'],
                book['total_copies'],
                book['available_copies'],
                book['status']
            )
            self.tree.insert('', 'end', values=values)

    def borrow_book(self):
        """借阅图书"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要借阅的图书！')
            return

        # 获取选中的图书数据
        item = self.tree.item(selected[0])
        values = item['values']

        # 检查是否可借
        if values[11] != '可借':
            messagebox.showwarning('提示', '该图书已无可借复本！')
            return

        if messagebox.askyesno('确认', f'确定要借阅《{values[2]}》吗？'):
            from models.borrow import BorrowManager
            success, message = BorrowManager.borrow_book(
                self.current_user['user_id'],
                values[0]  # book_id
            )
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)
