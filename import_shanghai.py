# import_shanghai.py
import sqlite3
import pandas as pd
from config import DB_PATH, CSV_DIR
import os


def import_shanghai_data():
    """导入上海财经大学数据"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. 插入上海财经大学
    cursor.execute("INSERT OR IGNORE INTO university (name, location) VALUES (?, ?)",
                   ("上海财经大学", "上海"))

    cursor.execute("SELECT id FROM university WHERE name = '上海财经大学'")
    shanghai_id = cursor.fetchone()[0]
    print(f"上海财经大学ID: {shanghai_id}")

    # 2. 读取上财课程数据
    csv_path = os.path.join(CSV_DIR, "上财_课程_手动录入.csv")

    if not os.path.exists(csv_path):
        print(f"❌ 文件不存在: {csv_path}")
        conn.close()
        return

    df = pd.read_csv(csv_path)
    print(f"读取到 {len(df)} 门课程")

    # 3. 按专业分组导入
    for major_name in df['major'].unique():
        major_df = df[df['major'] == major_name]

        # 检查专业是否已存在
        cursor.execute("SELECT id FROM major WHERE name = ? AND univ_id = ?",
                       (major_name, shanghai_id))
        existing = cursor.fetchone()

        if existing:
            major_id = existing[0]
            print(f"\n专业已存在: {major_name} (ID: {major_id})")
        else:
            # 插入专业
            total_credits = 150 if major_name == '金融学' else 155
            cursor.execute("""
                           INSERT INTO major (univ_id, name, college, total_credits)
                           VALUES (?, ?, ?, ?)
                           """, (shanghai_id, major_name, "上海财经大学", total_credits))
            major_id = cursor.lastrowid
            print(f"\n新增专业: {major_name} (ID: {major_id})")

        # 导入课程
        count = 0
        for _, row in major_df.iterrows():
            cursor.execute("""
                           INSERT
                           OR IGNORE INTO course (code, name, credit, hours, type)
                VALUES (?, ?, ?, ?, ?)
                           """, (row['code'], row['name'], row['credit'], row['hours'], row['type']))

            cursor.execute("SELECT id FROM course WHERE code = ?", (row['code'],))
            result = cursor.fetchone()

            if result:
                is_required = 1 if row['type'] == '必修' else 0
                cursor.execute("""
                               INSERT
                               OR IGNORE INTO program_course (major_id, course_id, is_required)
                    VALUES (?, ?, ?)
                               """, (major_id, result[0], is_required))
                count += 1

        print(f"  导入 {count} 门课程")

    conn.commit()
    conn.close()
    print("\n✅ 上财数据导入完成！")


def verify():
    """验证数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n" + "=" * 60)
    print("📊 数据库专业统计")
    print("=" * 60)

    cursor.execute("""
                   SELECT u.name, m.name, m.college, m.total_credits, COUNT(pc.course_id) as course_count
                   FROM major m
                            JOIN university u ON m.univ_id = u.id
                            LEFT JOIN program_course pc ON m.id = pc.major_id
                   GROUP BY m.id
                   ORDER BY u.name, m.name
                   """)

    print(f"{'大学':<12} | {'专业':<15} | {'学院':<12} | {'总学分':<8} | {'课程数'}")
    print("-" * 70)
    for row in cursor.fetchall():
        print(f"{row[0]:<12} | {row[1]:<15} | {row[2]:<12} | {row[3]:<8} | {row[4]}门")

    conn.close()


if __name__ == "__main__":
    import_shanghai_data()
    verify()