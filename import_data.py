# import_data.py
import sqlite3
import pandas as pd
from config import DB_PATH, CSV_DIR
import os


def import_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS university (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            location TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS major (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            univ_id INTEGER,
            name TEXT NOT NULL,
            college TEXT,
            total_credits REAL,
            FOREIGN KEY (univ_id) REFERENCES university(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT NOT NULL,
            credit REAL,
            hours INTEGER,
            type TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS program_course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            major_id INTEGER,
            course_id INTEGER,
            semester INTEGER,
            is_required BOOLEAN,
            FOREIGN KEY (major_id) REFERENCES major(id),
            FOREIGN KEY (course_id) REFERENCES course(id)
        )
    ''')

    # 插入大学
    cursor.execute("INSERT INTO university (name, location) VALUES (?, ?)",
                   ("西南财经大学", "四川成都"))
    univ_id = cursor.lastrowid

    # ========== 专业1：金融学 ==========
    cursor.execute("INSERT INTO major (univ_id, name, college, total_credits) VALUES (?, ?, ?, ?)",
                   (univ_id, "金融学", "金融学院", 150))
    major_id_1 = cursor.lastrowid

    # 读取金融学课程
    df1 = pd.read_csv(os.path.join(CSV_DIR, "1金融学类_cleaned.csv"))
    count1 = 0
    for _, row in df1.iterrows():
        cursor.execute("INSERT OR IGNORE INTO course (code, name, credit, hours, type) VALUES (?, ?, ?, ?, ?)",
                       (row['code'], row['name'], row['credit'], row['hours'], row['type']))
        cursor.execute("SELECT id FROM course WHERE code = ?", (row['code'],))
        result = cursor.fetchone()
        if result:
            course_id = result[0]
            cursor.execute("INSERT OR IGNORE INTO program_course (major_id, course_id, is_required) VALUES (?, ?, ?)",
                           (major_id_1, course_id, 1))
            count1 += 1

    # ========== 专业2：计算机科学与技术 ==========
    cursor.execute("INSERT INTO major (univ_id, name, college, total_credits) VALUES (?, ?, ?, ?)",
                   (univ_id, "计算机科学与技术", "计算机与人工智能学院", 160))
    major_id_2 = cursor.lastrowid

    # 读取计算机课程
    df2 = pd.read_csv(os.path.join(CSV_DIR, "20252025计算机类(2025计算机类)_cleaned.csv"))
    count2 = 0
    for _, row in df2.iterrows():
        cursor.execute("INSERT OR IGNORE INTO course (code, name, credit, hours, type) VALUES (?, ?, ?, ?, ?)",
                       (row['code'], row['name'], row['credit'], row['hours'], row['type']))
        cursor.execute("SELECT id FROM course WHERE code = ?", (row['code'],))
        result = cursor.fetchone()
        if result:
            course_id = result[0]
            cursor.execute("INSERT OR IGNORE INTO program_course (major_id, course_id, is_required) VALUES (?, ?, ?)",
                           (major_id_2, course_id, 1))
            count2 += 1

    # 先查询再关闭连接
    cursor.execute("SELECT COUNT(*) FROM course")
    course_count = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    print("=" * 50)
    print("导入完成！")
    print("=" * 50)
    print(f"金融学: {count1} 门课程")
    print(f"计算机科学与技术: {count2} 门课程")
    print(f"课程表总计: {course_count} 门课程")


if __name__ == "__main__":
    import_data()