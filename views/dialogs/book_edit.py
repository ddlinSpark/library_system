# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BookEditDialog(tk.Toplevel):
    def __init__(self, parent, title="添加图书", book_data=None, callback=None):
        super().__init__(parent)
        self.title(title)
        self.callback = callback
        self.book_data = book_data

        # 设置窗口属性
        self.geometry('600x700')
        self.resizable(False, False)
        self.transient(parent)  # 设置为父窗口的临时窗口
        self.grab_set()  # 模态窗口

        # 创建主容器
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True)

        # 创建画布和滚动条
        self.canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)

        # 创建可滚动框架
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 在画布上创建窗口
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # 布局管理
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 绑定鼠标滚轮事件
        self.bind_mouse_wheel()

        # 初始化界面
        self.init_ui()

        # 如果是编辑模式，填充数据
        if book_data:
            self.fill_data()

    def bind_mouse_wheel(self):
        """绑定鼠标滚轮事件"""

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")

        # 绑定鼠标进入和离开事件
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)

    def init_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.scrollable_frame, padding="20 10 20 10")
        main_frame.pack(fill='both', expand=True)

        # 表单框架
        form_frame = ttk.LabelFrame(main_frame, text='图书信息', padding=15)
        form_frame.pack(fill='x', padx=20)

        # ISBN
        isbn_frame = ttk.Frame(form_frame)
        isbn_frame.pack(fill='x', pady=5)

        ttk.Label(
            isbn_frame,
            text='ISBN:  *',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.isbn_var = tk.StringVar()
        self.isbn_entry = ttk.Entry(
            isbn_frame,
            textvariable=self.isbn_var,
            width=40
        )
        self.isbn_entry.pack(fill='x', pady=(2, 0))

        # 书名
        title_frame = ttk.Frame(form_frame)
        title_frame.pack(fill='x', pady=5)

        ttk.Label(
            title_frame,
            text='书名:  *',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(
            title_frame,
            textvariable=self.title_var,
            width=40
        )
        self.title_entry.pack(fill='x', pady=(2, 0))

        # 作者
        author_frame = ttk.Frame(form_frame)
        author_frame.pack(fill='x', pady=5)

        ttk.Label(
            author_frame,
            text='作者:  *',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(
            author_frame,
            textvariable=self.author_var,
            width=40
        )
        self.author_entry.pack(fill='x', pady=(2, 0))

        # 出版社
        publisher_frame = ttk.Frame(form_frame)
        publisher_frame.pack(fill='x', pady=5)

        ttk.Label(
            publisher_frame,
            text='出版社:  *',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.publisher_var = tk.StringVar()
        self.publisher_entry = ttk.Entry(
            publisher_frame,
            textvariable=self.publisher_var,
            width=40
        )
        self.publisher_entry.pack(fill='x', pady=(2, 0))

        # 出版日期
        date_frame = ttk.Frame(form_frame)
        date_frame.pack(fill='x', pady=5)

        ttk.Label(
            date_frame,
            text='出版日期:  *',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(
            date_frame,
            textvariable=self.date_var,
            width=40
        )
        self.date_entry.pack(fill='x', pady=(2, 0))
        ttk.Label(
            date_frame,
            text='格式：YYYY-MM-DD',
            font=('微软雅黑', 9),
            foreground='gray'
        ).pack(side='top', anchor='w')

        # 分类
        category_frame = ttk.Frame(form_frame)
        category_frame.pack(fill='x', pady=5)

        ttk.Label(
            category_frame,
            text='分类:',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.category_var = tk.StringVar()
        self.category_entry = ttk.Entry(
            category_frame,
            textvariable=self.category_var,
            width=40
        )
        self.category_entry.pack(fill='x', pady=(2, 0))

        # 馆藏位置
        location_frame = ttk.Frame(form_frame)
        location_frame.pack(fill='x', pady=5)

        ttk.Label(
            location_frame,
            text='馆藏位置:',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(
            location_frame,
            textvariable=self.location_var,
            width=40
        )
        self.location_entry.pack(fill='x', pady=(2, 0))

        # 价格
        price_frame = ttk.Frame(form_frame)
        price_frame.pack(fill='x', pady=5)

        ttk.Label(
            price_frame,
            text='价格:',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(
            price_frame,
            textvariable=self.price_var,
            width=40
        )
        self.price_entry.pack(fill='x', pady=(2, 0))

        # 总复本数
        copies_frame = ttk.Frame(form_frame)
        copies_frame.pack(fill='x', pady=5)

        ttk.Label(
            copies_frame,
            text='总复本数:  *',
            font=('微软雅黑', 10)
        ).pack(side='top', anchor='w')

        self.copies_var = tk.StringVar(value='1')
        self.copies_entry = ttk.Entry(
            copies_frame,
            textvariable=self.copies_var,
            width=40
        )
        self.copies_entry.pack(fill='x', pady=(2, 0))

        # 提示信息
        ttk.Label(
            main_frame,
            text='带 * 号的字段为必填项',
            font=('微软雅黑', 9),
            foreground='red'
        ).pack(pady=10)

        # 按钮框架 - 移到窗口底部固定位置
        button_frame = ttk.Frame(self)  # 注意这里使用self而不是main_frame
        button_frame.pack(side='bottom', pady=10)

        # 保存按钮
        save_btn = ttk.Button(
            button_frame,
            text='保存',
            command=self.save_book,
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

        # 调整画布大小
        self.scrollable_frame.update_idletasks()
        self.canvas.config(width=580, height=620)  # 预留按钮区域的空间

    def fill_data(self):
        """填充图书数据"""
        self.isbn_var.set(self.book_data['isbn'])
        self.title_var.set(self.book_data['title'])
        self.author_var.set(self.book_data['author'])
        self.publisher_var.set(self.book_data['publisher'])
        self.date_var.set(self.book_data['publish_date'])
        self.category_var.set(self.book_data['category'])
        self.location_var.set(self.book_data['location'])
        self.price_var.set(str(self.book_data['price']))
        self.copies_var.set(str(self.book_data['total_copies']))

    def validate_data(self):
        """验证数据"""
        # 获取并清理数据
        isbn = self.isbn_var.get().strip()
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        publisher = self.publisher_var.get().strip()
        publish_date = self.date_var.get().strip()
        category = self.category_var.get().strip()
        location = self.location_var.get().strip()
        price = self.price_var.get().strip()
        total_copies = self.copies_var.get().strip()

        # 验证必填字段
        if not all([isbn, title, author, publisher, publish_date, total_copies]):
            messagebox.showwarning('错误', '请填写所有必填字段！')
            return None

        # 验证日期格式
        try:
            datetime.strptime(publish_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning('错误', '出版日期格式不正确！\n正确格式：YYYY-MM-DD')
            return None

        # 验证价格格式
        if price:
            try:
                price = float(price)
                if price < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning('错误', '价格必须是非负数！')
                return None
        else:
            price = 0.00

        # 验证复本数
        try:
            total_copies = int(total_copies)
            if total_copies < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning('错误', '总复本数必须是正整数！')
            return None

        # 返回验证后的数据
        return {
            'isbn': isbn,
            'title': title,
            'author': author,
            'publisher': publisher,
            'publish_date': publish_date,
            'category': category,
            'location': location,
            'price': price,
            'total_copies': total_copies
        }

    def save_book(self):
        """保存图书信息"""
        data = self.validate_data()
        if data and self.callback:
            self.callback(data)
            self.destroy()
