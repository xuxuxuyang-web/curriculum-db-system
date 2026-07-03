<img width="829" height="463" alt="image" src="https://github.com/user-attachments/assets/0cd642c1-7b66-416d-aeab-93383d1af2a6" /># 📚 培养方案数据库系统

西南财经大学《数据库系统》课程设计项目

---

## 📖 项目简介

本项目设计并实现了一个培养方案数据库系统，以西南财经大学和上海财经大学
2025级本科培养方案为数据源，完成了从非结构化PDF文档到结构化关系型数据库的完整数据预处理流程，并提供CLI命令行界面 和 FastAPI Web界面两种交互方式，支持6类典型查询、自然语言查询和跨校对比分析。
---

## ✨ 功能特点

| 功能     | 说明 |
|--------|------|
| 数据预处理  | 从PDF自动提取表格数据，完成清洗与结构化处理 |
| 数据库设计  | 4张核心表，完整的主外键约束 |
| 6类典型查询 | 必修课列表、课程信息、总学分、开设专业、学院概览、关键词搜索 |
| 自然语言查询 | 支持中文问题自动转换为SQL |
| 双界面交互  | CLI命令行 + FastAPI Web界面 |
| 跨校对比分析 | 支持两校专业对比、课程数量对比、总学分对比 |
---

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.13 | 主要开发语言 |
| SQLite | 嵌入式数据库 |
| FastAPI | Web框架 |
| pdfplumber | PDF表格提取 |
| Pandas | 数据处理 |
| PrettyTable | CLI表格美化 |
| Jinja2 | HTML模板引擎 |
---

## 📁 项目结构


```
curriculum_db_system/
│
├── web_app.py                      # 🌐 Web界面主程序（FastAPI）
├── main.py                         # 💻 CLI命令行界面
├── init_db.py                      # 🗄️ 数据库初始化
├── import_data.py                  # 📥 西财数据导入模块
├── import_shanghai.py              # 📥 上财数据导入模块
├── clean_data.py                   # 🧹 数据清洗模块
├── extract_pdf.py                  # 📄 PDF表格提取模块
├── extract_shanghai_courses.py     # 📄 上财课程提取模块
├── query.py                        # 🔍 查询模块
├── nl_parser.py                    # 💬 自然语言解析模块
├── config.py                       # ⚙️ 配置文件
├── cross_compare.py                # 🔄 跨校对比模块
│
├── database/
│   └── curriculum.db               # SQLite数据库文件
│
├── data/
│   ├── pdf/                        # 原始PDF文件目录
│   │
│   └── csv/                        # 清洗后的CSV数据目录
│
├── templates/                      # Web页面模板目录
│   ├── index.html                  # 首页（6类查询卡片）
│   └── result.html                 # 结果展示页
│
├── .idea/                          # PyCharm IDE配置（可忽略）
├── __pycache__/                    # Python缓存文件（可忽略）
│
├── requirements.txt                # Python依赖列表
└── README.md                       # 项目说明文档
```
## 📊 数据统计

### 处理数据规模

| 专业 | 课程数量 | 学分范围 |
|------|----------|----------|
| 金融学 | 102门 | 0.5-6.0 |
| 计算机科学与技术 | 98门 | 0.5-6.0 |
| **合计** | **200门** | — |

### 学分分布

| 学分 | 课程数量 |
|------|----------|
| 0.5 | 4门 |
| 1.0 | 9门 |
| 2.0 | 41门 |
| 3.0 | 28门 |
| 4.0 | 7门 |
| 5.0 | 1门 |
| 6.0 | 3门 |

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/xuxuxuyang-web/curriculum-db-system.git
cd curriculum-db-system
```

### 2.创建虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python -m venv venv
source venv/bin/activate

```

### 3.安装依赖 
```bash
pip install -r requirements.txt
```

### 4.初始化数据库
```bash
python init_db.py
python import_data.py
```

### 5.运行系统
```bash
# Web界面（推荐）
python web_app.py

# CLI命令行界面
python main.py
```

### 6.访问Web界面
浏览器打开：http://127.0.0.1:8080

## 📝 使用示例

### Web界面功能

| 功能 | 输入示例 | 输出 |
|------|----------|------|
| 1. 查询专业必修课 | `金融学` | 102门课程列表 |
| 2. 查询课程信息 | `高等数学` | 学分5.0，学时85 |
| 3. 查询专业总学分 | `金融学` | 150学分 |
| 4. 查询开设专业 | `高等数学` | 开设该课程的专业列表 |
| 5. 查询学院专业 | `计算机` | 计算机学院专业概览 |
| 6. 关键词搜索 | `金融` | 22门相关课程 |

### 自然语言查询示例

| 自然语言问题 | 系统理解 |
|--------------|----------|
| "金融学专业必修课" | 查询必修课列表 |
| "高等数学课程的学分" | 查询课程信息 |
| "计算机科学与技术专业总学分" | 查询总学分 |
| "搜索金融课程" | 关键词模糊搜索 |

## 📄 数据库设计

### ER图

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   University    │     │      Major      │     │     Course      │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│  id (PK)        │◄─── │  univ_id (FK)   │     │  id (PK)        │
│  name           │     │  id (PK)        │     │  code           │
│  location       │     │  name           │     │  name           │
└─────────────────┘     │  college        │     │  credit         │
                        │  total_credits  │     │  hours          │
                        └─────────────────┘     │  type           │
                               │                └─────────────────┘
                               │                         │
                               │    ┌────────────────────┘
                               │    │
                        ┌──────▼────┴─────────────────────┐
                        │         ProgramCourse           │
                        ├─────────────────────────────────┤
                        │  id (PK)                        │
                        │  major_id (FK) ──► Major.id     │
                        │  course_id (FK) ──► Course.id   │
                        │  semester                       │
                        │  is_required                    │
                        └─────────────────────────────────┘
```

### 表结构说明

| 表名 | 说明 | 主键 | 外键 |
|------|------|------|------|
| university | 学校信息 | id | - |
| major | 专业信息 | id | univ_id → university.id |
| course | 课程信息 | id | - |
| program_course | 培养方案关联 | id | major_id → major.id, course_id → course.id |

### 字段详细说明

#### university（学校表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY | 学校ID |
| name | VARCHAR(100) | NOT NULL | 学校名称 |
| location | VARCHAR(100) | - | 所在地 |

#### major（专业表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY | 专业ID |
| univ_id | INTEGER | FOREIGN KEY | 所属大学 |
| name | VARCHAR(100) | NOT NULL | 专业名称 |
| college | VARCHAR(100) | - | 所属学院 |
| total_credits | DECIMAL(5,1) | - | 总学分要求 |

#### course（课程表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY | 课程ID |
| code | VARCHAR(20) | UNIQUE | 课程代码 |
| name | VARCHAR(200) | NOT NULL | 课程名称 |
| credit | DECIMAL(3,1) | - | 学分 |
| hours | INTEGER | - | 学时 |
| type | VARCHAR(50) | - | 课程类型（必修/选修） |

#### program_course（培养方案关联表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY | 关联ID |
| major_id | INTEGER | FOREIGN KEY | 专业ID |
| course_id | INTEGER | FOREIGN KEY | 课程ID |
| semester | INTEGER | - | 建议修读学期 |
| is_required | BOOLEAN | DEFAULT 1 | 是否必修 |
