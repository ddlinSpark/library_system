# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from views.dialogs.book_edit import BookEditDialog
from models.book import BookManager
import logging

logger = logging.getLogger(__name__)


class BookManageView(ttk.Frame):
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
        self.search_type = tk.StringVar(value='book_id')
        search_type_frame = ttk.Frame(search_frame)
        search_type_frame.pack(side='left', padx=5)

        ttk.Radiobutton(
            search_type_frame,
            text='ID',
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
            command=self.search_books,
            width=10
        ).pack(side='left', padx=5)

        # 操作按钮
        btn_frame = ttk.Frame(toolbar_frame)
        btn_frame.pack(side='right', padx=5)

        ttk.Button(
            btn_frame,
            text='添加图书',
            command=self.add_book,
            width=15
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text='编辑图书',
            command=self.edit_book,
            width=15
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text='删除图书',
            command=self.delete_book,
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
            if col in ['book_id', 'total_copies', 'available_copies']:
                width = 70
            elif col in ['isbn', 'publish_date', 'category', 'location', 'price', 'status']:
                width = 100
            else:
                width = 150
            self.tree.column(col, width=width, anchor='center')

        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill='both', expand=True)

        # 绑定双击事件
        self.tree.bind('<Double-1>', lambda e: self.edit_book())

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

        # 验证搜索条件
        if self.search_type.get() == 'book_id':
            try:
                book_id = int(keyword)
            except ValueError:
                messagebox.showwarning('错误', 'ID必须是数字！')
                return

        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 搜索并显示结果
        books = BookManager.search_books(keyword, self.search_type.get())
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

    def add_book(self):
        """添加图书"""

        def on_book_add(book_data):
            success, message = BookManager.add_book(book_data)
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)

        BookEditDialog(self, callback=on_book_add)

    def edit_book(self):
        """编辑图书"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要编辑的图书！')
            return

        # 获取选中的图书数据
        item = self.tree.item(selected[0])
        values = item['values']
        book_data = {
            'book_id': values[0],
            'isbn': values[1],
            'title': values[2],
            'author': values[3],
            'publisher': values[4],
            'publish_date': values[5],
            'category': values[6],
            'location': values[7],
            'price': values[8],
            'total_copies': values[9],
            'available_copies': values[10]
        }

        def on_book_edit(new_data):
            success, message = BookManager.update_book(book_data['book_id'], new_data)
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)

        BookEditDialog(
            self,
            title="编辑图书",
            book_data=book_data,
            callback=on_book_edit
        )

    def delete_book(self):
        """删除图书"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('提示', '请先选择要删除的图书！')
            return

        book_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno('确认', '确定要删除选择的图书吗？'):
            success, message = BookManager.delete_book(book_id)
            if success:
                messagebox.showinfo('成功', message)
                self.refresh_table()
            else:
                messagebox.showerror('错误', message)
