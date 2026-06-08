# config.py
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据路径
PDF_DIR = os.path.join(BASE_DIR, "data", "pdf")
CSV_DIR = os.path.join(BASE_DIR, "data", "csv")
DB_PATH = os.path.join(BASE_DIR, "database", "curriculum.db")

# 确保目录存在
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)