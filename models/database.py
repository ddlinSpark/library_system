# -*- coding: utf-8 -*-
import mysql.connector
import logging
from tkinter import messagebox

logger = logging.getLogger(__name__)


def get_connection():
    """获取数据库连接"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="library",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            use_unicode=True
        )
        """
        两个数据库源
        
        本地服务(localhost)
            host="localhost",
            user="root",
            password="123456",
            database="library",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            use_unicode=True
        远程轻量级服务器(8.155.21.3)
            host="8.155.21.3",
            user="admin",
            password="8M0x7G0P7UCdpFdL3HzyRDHZzRy1x0",
            database="library",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            use_unicode=True
        """
        cursor = conn.cursor()
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute('SET CHARACTER SET utf8mb4')
        cursor.execute('SET character_set_connection=utf8mb4')
        cursor.close()
        return conn
    except mysql.connector.Error as err:
        logger.error(f"数据库连接错误: {err}")
        return None


def test_connection():
    """测试数据库连接"""
    conn = get_connection()
    if conn:
        logger.info("数据库连接测试成功")
        conn.close()
        return True
    else:
        logger.error("数据库连接测试失败")
        return False


if __name__ == "__main__":
    # 仅在直接运行此文件时配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    test_connection()
