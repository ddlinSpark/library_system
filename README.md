# 图书管理系统 (library_system)

## 项目概述

图书管理系统是一个用于管理图书馆书籍的软件。它允许用户添加、删除、搜索和更新书籍信息。该系统旨在提高图书馆的管理效率，方便用户进行书籍的借阅和归还操作。

## 功能特性

- **用户管理**：支持多用户管理，用户可以根据角色（管理员或普通用户）进行不同的操作。
- **书籍管理**：用户可以添加新书籍、删除现有书籍、更新书籍信息以及搜索书籍。
- **借阅管理**：系统记录书籍的借阅和归还情况，用户可以查看自己的借阅记录。
- **数据统计**：提供书籍的借阅统计信息，帮助管理员了解书籍的使用情况。

## 技术栈

- **前端**：使用 Python 的 Tkinter 库构建图形用户界面。
- **后端**：使用 Python 进行业务逻辑处理，连接 MySQL 数据库进行数据存储。
- **数据库**：使用 MySQL 存储用户信息、书籍信息和借阅记录。

## 安装指南

1. 克隆仓库到本地：

   ```shell
   git clone https://github.com/your-username/library_system.git
   cd library_system
   ```

2. 安装依赖

   在安装依赖之前，请确保你已经安装了 Python 3.x 和 pip。你可以通过以下命令检查 Python 和 pip 的版本：

   ```shell
   python --version
   pip --version
   ```

   如果没有安装 Python，请访问 [Python 官网](https://www.python.org/downloads/) 下载并安装。

   然后，使用以下命令安装项目所需的依赖：

   ```shell
   pip install Flask==2.0.3
   pip install Flask-MySQLdb==1.0.0
   pip install mysql-connector-python==8.0.28
   ```

3. 运行程序

   ```shell
   python run.py
   ```

   确保在运行程序之前，数据库已正确配置并初始化（请参考 `library.sql` 文件以获取数据库结构和初始数据）。

## 使用说明

- **添加书籍**：通过命令行或界面添加新书籍。
- **删除书籍**：通过书籍ID删除书籍。
- **搜索书籍**：根据书名、作者等信息搜索书籍。
- **更新书籍**：更新书籍的详细信息。
- **借阅书籍**：用户可以借阅书籍并查看借阅记录。
- **归还书籍**：用户可以归还已借阅的书籍。

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目。
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 打开一个 Pull Request。

## 许可证

本项目采用 MIT 许可证。请参阅 [LICENSE](LICENSE) 文件获取更多信息。

## 联系方式

如有任何问题或建议，请联系开发团队：

- **开发团队**：林华东、黄鸿乐、韦嘉豪
- **邮箱**：3380845753@qq.com

## 项目结构

```
library_system/
│
├── models/                 # 存放数据模型
│   ├── book.py            # 书籍管理
│   ├── borrow.py          # 借阅管理
│   ├── database.py        # 数据库连接管理
│   └── user.py            # 用户管理
│
├── views/                  # 存放视图相关的文件
│   ├── login.py           # 登录窗口
│   ├── main.py            # 主窗口
│   ├── register.py        # 注册窗口
│   ├── __init__.py        # 标记为Python包
│   │
│   ├── dialogs/           # 弹出对话框
│   │   ├── book_edit.py     # 编辑书籍对话框
│   │   ├── user_edit.py     # 编辑用户对话框
│   │   └── __pycache__      # 编译缓存文件
│   │
│   └── pages/             # 各个功能页面
│       ├── about.py          # 关于页面
│       ├── book_manage.py     # 书籍管理页面
│       ├── book_search.py      # 书籍搜索页面
│       ├── borrow_manage.py     # 借阅管理页面
│       ├── home.py           # 首页
│       ├── my_borrows.py     # 我的借阅记录页面
│       ├── profile.py        # 用户个人资料页面
│       └── user_manage.py    # 用户管理页面
│
├── library.sql             # 数据库初始化脚本
├── README.md                # 项目说明文档
├── run.cmd                 # 启动脚本
└── run.py                  # 启动程序
```

## 未来计划

- 增加书籍预约功能。
- 提供用户反馈和评价系统。
- 实现数据导出功能，支持导出借阅记录和书籍信息。
- 增强用户界面，提升用户体验。

## 常见问题

- **如何重置密码？**  
  用户可以通过注册页面的“忘记密码”链接重置密码。

- **如何联系支持团队？**  
  请通过上面的联系方式与开发团队联系。

- **是否支持多语言？**  
  目前系统仅支持中文，未来计划增加其他语言支持。


