# -*- coding: utf-8 -*-
from .database import get_connection
import mysql.connector
import logging

logger = logging.getLogger(__name__)


class BookManager:
    @staticmethod
    def get_all_books():
        """获取所有图书"""
        conn = get_connection()
        if not conn:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT book_id, isbn, title, author, publisher,
                       DATE_FORMAT(publish_date, '%Y-%m-%d') as publish_date,
                       category, location, price, total_copies,
                       available_copies,
                       CASE 
                           WHEN available_copies > 0 THEN '可借'
                           ELSE '已借完'
                       END as status
                FROM books
                ORDER BY book_id DESC
            """)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            logger.error(f"获取图书列表错误: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def search_books(keyword, search_type='book_id'):
        """搜索图书
        
        Args:
            keyword: 搜索关键词
            search_type: 搜索类型，可选值：book_id
        """
        conn = get_connection()
        if not conn:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            if search_type == 'book_id':
                # 按ID精确搜索
                cursor.execute("""
                    SELECT book_id, isbn, title, author, publisher,
                           DATE_FORMAT(publish_date, '%Y-%m-%d') as publish_date,
                           category, location, price, total_copies,
                           available_copies,
                           CASE 
                               WHEN available_copies > 0 THEN '可借'
                               ELSE '已借完'
                           END as status
                    FROM books
                    WHERE book_id = %s
                """, (keyword,))
            else:
                logger.warning(f"未知的搜索类型: {search_type}")
                return []

            return cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"搜索图书错误: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def add_book(book_data):
        """添加图书"""
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO books (
                    isbn, title, author, publisher, publish_date,
                    category, location, price, total_copies, available_copies
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                book_data['isbn'],
                book_data['title'],
                book_data['author'],
                book_data['publisher'],
                book_data['publish_date'],
                book_data['category'],
                book_data['location'],
                book_data['price'],
                book_data['total_copies'],
                book_data['total_copies']  # 初始可借数量等于总数量
            ))

            conn.commit()
            return True, "图书添加成功"

        except mysql.connector.Error as err:
            logger.error(f"添加图书错误: {err}")
            return False, f"添加图书失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def update_book(book_id, book_data):
        """更新图书信息"""
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"

        cursor = None
        try:
            cursor = conn.cursor()

            # 先获取原有的总数量和可借数量
            cursor.execute(
                "SELECT total_copies, available_copies FROM books WHERE book_id = %s",
                (book_id,)
            )
            old_data = cursor.fetchone()
            if not old_data:
                return False, "图书不存在"

            old_total, old_available = old_data

            # 计算新的可借数量
            new_total = int(book_data['total_copies'])
            if new_total < old_total - old_available:  # 新总数不能小于已借出数量
                return False, "新的总数量不能小于已借出的数量"

            new_available = old_available + (new_total - old_total)

            cursor.execute("""
                UPDATE books SET
                    isbn = %s,
                    title = %s,
                    author = %s,
                    publisher = %s,
                    publish_date = %s,
                    category = %s,
                    location = %s,
                    price = %s,
                    total_copies = %s,
                    available_copies = %s
                WHERE book_id = %s
            """, (
                book_data['isbn'],
                book_data['title'],
                book_data['author'],
                book_data['publisher'],
                book_data['publish_date'],
                book_data['category'],
                book_data['location'],
                book_data['price'],
                new_total,
                new_available,
                book_id
            ))

            conn.commit()
            return True, "图书信息更新成功"

        except mysql.connector.Error as err:
            logger.error(f"更新图书错误: {err}")
            return False, f"更新图书失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def delete_book(book_id):
        """删除图书"""
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"

        cursor = None
        try:
            cursor = conn.cursor()

            # 检查是否有未还的借阅记录
            cursor.execute("""
                SELECT COUNT(*) FROM borrowing_records 
                WHERE book_id = %s AND status = 'borrowed'
            """, (book_id,))

            if cursor.fetchone()[0] > 0:
                return False, "该图书还有未还的借阅记录，无法删除"

            cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
            conn.commit()

            if cursor.rowcount == 0:
                return False, "图书不存在"

            return True, "图书删除成功"

        except mysql.connector.Error as err:
            logger.error(f"删除图书错误: {err}")
            return False, f"删除图书失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def search_books_by_keyword(keyword, search_type='title'):
        """按关键词搜索图书
        
        Args:
            keyword: 搜索关键词
            search_type: 搜索类型，可选值：title, author, isbn
        """
        conn = get_connection()
        if not conn:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            # 构建查询条件
            if search_type == 'isbn':
                # ISBN精确匹配
                where_clause = "isbn = %s"
                params = [keyword]
            else:
                # 书名和作者模糊匹配
                where_clause = f"{search_type} LIKE %s"
                params = [f"%{keyword}%"]

            cursor.execute(f"""
                SELECT book_id, isbn, title, author, publisher,
                       DATE_FORMAT(publish_date, '%Y-%m-%d') as publish_date,
                       category, location, price, total_copies,
                       available_copies,
                       CASE 
                           WHEN available_copies > 0 THEN '可借'
                           ELSE '已借完'
                       END as status
                FROM books
                WHERE {where_clause}
                ORDER BY book_id DESC
            """, params)

            return cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"搜索图书错误: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()
