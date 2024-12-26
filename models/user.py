from .database import get_connection
import mysql.connector
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserManager:
    @staticmethod
    def verify_user(username, password, role=None):
        """验证用户登录"""
        conn = get_connection()
        if not conn:
            logger.error("数据库连接失败")
            return None
        
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 添加角色验证
            query = """
                SELECT user_id, username, role, real_name, status,
                       phone, email, created_at, last_login
                FROM users 
                WHERE username = %s AND password = %s AND status = 1
            """
            params = [username, password]
            
            if role:  # 如果指定了角色，添加角色验证
                query += " AND role = %s"
                params.append(role)
                
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            if result:
                # 更新最后登录时间
                cursor.execute("""
                    UPDATE users 
                    SET last_login = %s 
                    WHERE user_id = %s
                """, (datetime.now(), result['user_id']))
                conn.commit()
                
            logger.info(f"用户验证结果: {result}")
            return result
            
        except mysql.connector.Error as err:
            logger.error(f"数据库查询错误: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def register_user(username, password, real_name, phone=None, email=None):
        """注册新用户"""
        conn = get_connection()
        if not conn:
            logger.error("数据库连接失败")
            return False, "数据库连接失败"
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            # 检查用户名是否已存在
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return False, "用户名已存在"
            
            # 插入新用户
            cursor.execute("""
                INSERT INTO users (username, password, role, real_name, phone, email) 
                VALUES (%s, %s, 'user', %s, %s, %s)
            """, (username, password, real_name, phone, email))
            
            conn.commit()
            logger.info(f"新用户注册成功: {username}")
            return True, "注册成功"
            
        except mysql.connector.Error as err:
            logger.error(f"用户注册错误: {err}")
            return False, f"注册失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def get_user_info(user_id):
        """获取用户信息"""
        conn = get_connection()
        if not conn:
            return None
        
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT user_id, username, role, real_name, phone, email, created_at, last_login 
                FROM users 
                WHERE user_id = %s
            """, (user_id,))
            return cursor.fetchone()
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def get_all_users():
        """获取所有用户"""
        conn = get_connection()
        if not conn:
            return []
        
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT user_id, username, role, real_name, phone,
                       email, created_at, last_login, status
                FROM users
                ORDER BY user_id DESC
            """)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            logger.error(f"获取用户列表错误: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    @staticmethod
    def search_users(keyword, search_type='user_id'):
        """搜索用户
        
        Args:
            keyword: 搜索关键词
            search_type: 搜索类型，可选值：user_id
        """
        conn = get_connection()
        if not conn:
            return []
        
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            
            if search_type == 'user_id':
                # 按ID精确搜索
                cursor.execute("""
                    SELECT user_id, username, role, real_name, phone,
                           email, created_at, last_login, status
                    FROM users
                    WHERE user_id = %s
                """, (keyword,))
            else:
                logger.warning(f"未知的搜索类型: {search_type}")
                return []
                
            return cursor.fetchall()
            
        except mysql.connector.Error as err:
            logger.error(f"搜索用户错误: {err}")
            return []
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    @staticmethod
    def update_user_status(user_id, status):
        """更新用户状态
        
        Args:
            user_id: 用户ID
            status: 状态（0-禁用，1-启用）
        """
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            # 检查是否为管理员
            cursor.execute(
                "SELECT role FROM users WHERE user_id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
            if not user:
                return False, "用户不存在"
                
            if user[0] == 'admin':
                return False, "不能修改管理员账号的状态"
            
            cursor.execute("""
                UPDATE users 
                SET status = %s
                WHERE user_id = %s
            """, (status, user_id))
            
            conn.commit()
            action = "启用" if status == 1 else "禁用"
            return True, f"用户{action}成功"
            
        except mysql.connector.Error as err:
            logger.error(f"更新用户状态错误: {err}")
            return False, f"更新用户状态失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()
    
    @staticmethod
    def reset_password(user_id):
        """重置用户密码为123456"""
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            # 检查是否为管理员
            cursor.execute(
                "SELECT role FROM users WHERE user_id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
            if not user:
                return False, "用户不存在"
                
            if user[0] == 'admin':
                return False, "不能重置管理员账号的密码"
            
            cursor.execute("""
                UPDATE users 
                SET password = '123456'
                WHERE user_id = %s
            """, (user_id,))
            
            conn.commit()
            return True, "密码重置成功"
            
        except mysql.connector.Error as err:
            logger.error(f"重置密码错误: {err}")
            return False, f"重置密码失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def update_user_info(user_id, user_data):
        """更新用户信息
        
        Args:
            user_id: 用户ID
            user_data: 用户数据字典，包含 real_name, phone, email
        """
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users 
                SET real_name = %s,
                    phone = %s,
                    email = %s
                WHERE user_id = %s
            """, (
                user_data['real_name'],
                user_data['phone'],
                user_data['email'],
                user_id
            ))
            
            conn.commit()
            return True, "用户信息更新成功"
            
        except mysql.connector.Error as err:
            logger.error(f"更新用户信息错误: {err}")
            return False, f"更新用户信息失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """修改密码
        
        Args:
            user_id: 用户ID
            old_password: 原密码
            new_password: 新密码
        """
        conn = get_connection()
        if not conn:
            return False, "数据库连接失败"
        
        cursor = None
        try:
            cursor = conn.cursor()
            
            # 验证原密码
            cursor.execute("""
                SELECT user_id FROM users 
                WHERE user_id = %s AND password = %s
            """, (user_id, old_password))
            
            if not cursor.fetchone():
                return False, "原密码错误"
            
            # 更新密码
            cursor.execute("""
                UPDATE users 
                SET password = %s
                WHERE user_id = %s
            """, (new_password, user_id))
            
            conn.commit()
            return True, "密码修改成功"
            
        except mysql.connector.Error as err:
            logger.error(f"修改密码错误: {err}")
            return False, f"修改密码失败: {str(err)}"
        finally:
            if cursor:
                cursor.close()
            conn.close()
