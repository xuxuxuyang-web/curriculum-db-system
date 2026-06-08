# init_db.py
import sqlite3
from config import DB_PATH
import os


def init_database():
    """初始化数据库"""

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"已删除旧数据库")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建表
    cursor.execute('''
        CREATE TABLE university (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            location TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE major (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            univ_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            college TEXT,
            total_credits REAL,
            FOREIGN KEY (univ_id) REFERENCES university(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT NOT NULL,
            credit REAL,
            hours INTEGER,
            type TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE program_course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            major_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            semester INTEGER,
            is_required BOOLEAN DEFAULT 1,
            FOREIGN KEY (major_id) REFERENCES major(id),
            FOREIGN KEY (course_id) REFERENCES course(id)
        )
    ''')

    conn.commit()
    conn.close()

    print("数据库初始化成功！")
    print(f"数据库路径: {DB_PATH}")


if __name__ == "__main__":
    init_database()