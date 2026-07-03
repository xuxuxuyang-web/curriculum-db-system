# cross_compare.py
import sqlite3
from config import DB_PATH
from prettytable import PrettyTable


def run_tests():
    print("\n" + "=" * 70)
    print("🔬 跨校对比分析 - 5个测试用例")
    print("=" * 70)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 测试1：金融学总学分对比
    print("\n【测试用例1】对比金融学专业总学分要求")
    print("-" * 50)
    cursor.execute("""
                   SELECT u.name, m.total_credits
                   FROM major m
                            JOIN university u ON m.univ_id = u.id
                   WHERE m.name = '金融学'
                   ORDER BY u.name
                   """)
    results = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["大学", "总学分"]
    for row in results:
        table.add_row(row)
    print(table)

    # 测试2：计算机专业总学分对比
    print("\n【测试用例2】对比计算机科学与技术专业总学分要求")
    print("-" * 50)
    cursor.execute("""
                   SELECT u.name, m.total_credits
                   FROM major m
                            JOIN university u ON m.univ_id = u.id
                   WHERE m.name = '计算机科学与技术'
                   ORDER BY u.name
                   """)
    results = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["大学", "总学分"]
    for row in results:
        table.add_row(row)
    print(table)

    # 测试3：金融学课程数量对比
    print("\n【测试用例3】对比金融学专业课程数量")
    print("-" * 50)
    cursor.execute("""
                   SELECT u.name, COUNT(c.id) as course_count
                   FROM course c
                            JOIN program_course pc ON c.id = pc.course_id
                            JOIN major m ON pc.major_id = m.id
                            JOIN university u ON m.univ_id = u.id
                   WHERE m.name = '金融学'
                   GROUP BY u.name
                   """)
    results = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["大学", "课程数量"]
    for row in results:
        table.add_row(row)
    print(table)

    # 测试4：计算机课程数量对比
    print("\n【测试用例4】对比计算机科学与技术专业课程数量")
    print("-" * 50)
    cursor.execute("""
                   SELECT u.name, COUNT(c.id) as course_count
                   FROM course c
                            JOIN program_course pc ON c.id = pc.course_id
                            JOIN major m ON pc.major_id = m.id
                            JOIN university u ON m.univ_id = u.id
                   WHERE m.name = '计算机科学与技术'
                   GROUP BY u.name
                   """)
    results = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["大学", "课程数量"]
    for row in results:
        table.add_row(row)
    print(table)

    # 测试5：所有专业概览
    print("\n【测试用例5】所有专业概览")
    print("-" * 50)
    cursor.execute("""
                   SELECT u.name, m.name, m.total_credits, COUNT(pc.course_id) as course_count
                   FROM major m
                            JOIN university u ON m.univ_id = u.id
                            LEFT JOIN program_course pc ON m.id = pc.major_id
                   GROUP BY m.id
                   ORDER BY u.name, m.name
                   """)
    results = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["大学", "专业", "总学分", "课程数"]
    for row in results:
        table.add_row([row[0], row[1], row[2], f"{row[3]}门"])
    print(table)

    conn.close()
    print("\n" + "=" * 70)
    print("✅ 测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()