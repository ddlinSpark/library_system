# -*- coding: utf-8 -*-
import logging
import sys
from views.main import MainWindow
import tkinter as tk
from tkinter import messagebox

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    try:
        window = MainWindow()
        if window.winfo_exists():  # 检查窗口是否创建成功
            window.mainloop()
    except Exception as e:
        logger.error(f"程序运行错误: {e}")
        if tk._default_root:  # 如果主窗口存在
            messagebox.showerror(
                '错误', f'程序运行出错：\n{str(e)}\n\n请检查日志获取详细信息。'
            )
        sys.exit(1)


if __name__ == "__main__":
    main()
