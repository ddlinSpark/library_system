# -*- coding: utf-8 -*-
from .database import get_connection
import mysql.connector
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BorrowManager:
    @staticmethod
    def get_all_records():
        """获取所有借阅记录"""
        conn = get_connection()
        if not conn:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT br.record_id, br.book_id, b.title as book_title,
                       br.user_id, u.username,
                       DATE_FORMAT(br.borrow_date, '%Y-%m-%d') as borrow_date,
                       DATE_FORMAT(br.due_date, '%Y-%m-%d') as due_date,
                       DATE_FORMAT(br.return_date, '%Y-%m-%d') as return_date,
                       br.status
                FROM borrowing_records br
                JOIN books b ON br.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                ORDER BY br.record_id DESC
            """)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            logger.error(f"获取借阅记录列表错误: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def search_records(keyword, search_type='record_id'):
        """搜索借阅记录
        
        Args:
            keyword: 搜索关键词
            search_type: 搜索类型，可选值：record_id, user_id, book_id
        """
        conn = get_connection()
        if not conn:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT br.record_id, br.book_id, b.title as book_title,
                       br.user_id, u.username,
                       DATE_FORMAT(br.borrow_date, '%Y-%m-%d') as borrow_date,
                       DATE_FORMAT(br.due_date, '%Y-%m-%d') as due_date,
                       DATE_FORMAT(br.return_date, '%Y-%m-%d') as return_date,
                       br.status
                FROM borrowing_records br
                JOIN books b ON br.book_id = b.book_id
                JOIN users u ON br.user_id = u.user_id
                WHERE br.{} = %s
                ORDER BY br.record_id DESC
            """.format(search_type)

            cursor.execute(query, (keyword,))
            return cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"搜索借阅记录错误: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def borrow_book(user_id, book_id):
        """借阅图书
        
        Args:
            user_id: 用户ID
            book_id: 图书ID
        """
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"

        cursor = None
        try:
            cursor = conn.cursor()

            # 检查图书是否可借
            cursor.execute("""
                SELECT available_copies 
                FROM books 
                WHERE book_id = %s
            """, (book_id,))

            result = cursor.fetchone()
            if not result:
                return False, "图书不存在"

            if result[0] <= 0:
                return False, "该图书已无可借复本"

            # 检查用户是否有未还的相同图书
            cursor.execute("""
                SELECT COUNT(*) 
                FROM borrowing_records 
                WHERE user_id = %s AND book_id = %s AND status = 'borrowed'
            """, (user_id, book_id))

            if cursor.fetchone()[0] > 0:
                return False, "您已借阅过该图书且尚未归还"

            # 创建借阅记录
            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=30)  # 默认借期30天

            cursor.execute("""
                INSERT INTO borrowing_records 
                (user_id, book_id, borrow_date, due_date, status)
                VALUES (%s, %s, %s, %s, 'borrowed')
            """, (user_id, book_id, borrow_date, due_date))

            # 更新图书可借复本数
            cursor.execute("""
                UPDATE books 
                SET available_copies = available_copies - 1
                WHERE book_id = %s
            """, (book_id,))

            conn.commit()
            return True, "借阅成功"

        except mysql.connector.Error as err:
            logger.error(f"借阅图书错误: {err}")
            return False, f"借阅失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def return_book(record_id):
        """归还图书
        
        Args:
            record_id: 借阅记录ID
        """
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"

        cursor = None
        try:
            cursor = conn.cursor()

            # 获取借阅记录信息
            cursor.execute("""
                SELECT book_id, status
                FROM borrowing_records 
                WHERE record_id = %s
            """, (record_id,))

            result = cursor.fetchone()
            if not result:
                return False, "借阅记录不存在"

            if result[1] == 'returned':
                return False, "该图书已经归还"

            # 检查是否超期
            is_overdue, overdue_message = BorrowManager.check_overdue(record_id)

            # 更新借阅记录
            return_date = datetime.now().date()
            cursor.execute("""
                UPDATE borrowing_records 
                SET status = 'returned',
                    return_date = %s
                WHERE record_id = %s
            """, (return_date, record_id))

            # 更新图书可借复本数
            cursor.execute("""
                UPDATE books 
                SET available_copies = available_copies + 1
                WHERE book_id = %s
            """, (result[0],))

            conn.commit()
            return True, f"归还成功{overdue_message}"

        except mysql.connector.Error as err:
            logger.error(f"归还图书错误: {err}")
            return False, f"归还失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def get_user_records(user_id, status='all'):
        """获取用户的借阅记录
        
        Args:
            user_id: 用户ID
            status: 状态筛选，可选值：all, borrowed, returned
        """
        conn = get_connection()
        if not conn:
            return []

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT br.record_id, br.book_id, b.title as book_title,
                       DATE_FORMAT(br.borrow_date, '%Y-%m-%d') as borrow_date,
                       DATE_FORMAT(br.due_date, '%Y-%m-%d') as due_date,
                       DATE_FORMAT(br.return_date, '%Y-%m-%d') as return_date,
                       br.status
                FROM borrowing_records br
                JOIN books b ON br.book_id = b.book_id
                WHERE br.user_id = %s
            """

            params = [user_id]

            if status != 'all':
                query += " AND br.status = %s"
                params.append(status)

            query += " ORDER BY br.record_id DESC"

            cursor.execute(query, params)
            return cursor.fetchall()

        except mysql.connector.Error as err:
            logger.error(f"获取用户借阅记录错误: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def check_overdue(record_id):
        """检查是否超期
        
        Args:
            record_id: 借阅记录ID
            
        Returns:
            (bool, str): (是否超期, 超期信息)
        """
        conn = get_connection()
        if not conn:
            return False, ""

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT DATEDIFF(CURDATE(), due_date) as overdue_days
                FROM borrowing_records 
                WHERE record_id = %s AND status = 'borrowed'
            """, (record_id,))

            result = cursor.fetchone()
            if not result:
                return False, ""

            overdue_days = result['overdue_days']
            if overdue_days > 0:
                return True, f"\n该图书已超期 {overdue_days} 天，请尽快归还！"

            return False, ""

        except mysql.connector.Error as err:
            logger.error(f"检查超期错误: {err}")
            return False, ""
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def renew_book(record_id):
        """续借图书
        
        Args:
            record_id: 借阅记录ID
        """
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"

        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)

            # 获取借阅记录信息
            cursor.execute("""
                SELECT br.book_id, br.status, br.due_date,
                       (SELECT COUNT(*) FROM borrowing_records 
                        WHERE record_id = %s AND renew_count >= 2) as renewed_times
                FROM borrowing_records br
                WHERE br.record_id = %s
            """, (record_id, record_id))

            result = cursor.fetchone()
            if not result:
                return False, "借阅记录不存在"

            if result['status'] == 'returned':
                return False, "该图书已经归还，无法续借"

            if result['renewed_times'] > 0:
                return False, "该图书已续借过2次，无法继续续借"

            # 检查是否超期
            is_overdue, overdue_message = BorrowManager.check_overdue(record_id)
            if is_overdue:
                return False, "该图书已超期，请先归还"

            # 更新借阅记录
            new_due_date = datetime.strptime(result['due_date'], '%Y-%m-%d').date() + timedelta(days=30)
            cursor.execute("""
                UPDATE borrowing_records 
                SET due_date = %s,
                    renew_count = renew_count + 1
                WHERE record_id = %s
            """, (new_due_date, record_id))

            conn.commit()
            return True, f"续借成功，新的应还日期为：{new_due_date.strftime('%Y-%m-%d')}"

        except mysql.connector.Error as err:
            logger.error(f"续借图书错误: {err}")
            return False, f"续借失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()
