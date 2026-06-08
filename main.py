# main.py
import sys
import sqlite3
import re
from config import DB_PATH
from prettytable import PrettyTable


class CurriculumQuery:
    """培养方案查询系统"""

    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def get_required_courses(self, major_name, univ_name=None):
        """1. 查询某专业的必修课列表"""
        query = """
            SELECT c.code, c.name, c.credit, c.hours
            FROM course c
            JOIN program_course pc ON c.id = pc.course_id
            JOIN major m ON pc.major_id = m.id
            WHERE m.name LIKE ? AND pc.is_required = 1
        """
        params = [f'%{major_name}%']

        if univ_name:
            query += " AND m.univ_id = (SELECT id FROM university WHERE name LIKE ?)"
            params.append(f'%{univ_name}%')

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_course_info(self, course_name):
        """2. 查询某门课程的学分、学时信息"""
        query = """
            SELECT code, name, credit, hours, type
            FROM course
            WHERE name LIKE ?
            LIMIT 10
        """
        self.cursor.execute(query, (f'%{course_name}%',))
        return self.cursor.fetchall()

    def get_major_total_credits(self, major_name):
        """3. 查询某专业的总学分要求"""
        query = """
            SELECT name, total_credits
            FROM major
            WHERE name LIKE ?
        """
        self.cursor.execute(query, (f'%{major_name}%',))
        return self.cursor.fetchone()

    def get_majors_by_course(self, course_name):
        """4. 查询开设某门课程的所有专业"""
        query = """
            SELECT DISTINCT m.name, u.name as university
            FROM major m
            JOIN university u ON m.univ_id = u.id
            JOIN program_course pc ON m.id = pc.major_id
            JOIN course c ON pc.course_id = c.id
            WHERE c.name LIKE ?
        """
        self.cursor.execute(query, (f'%{course_name}%',))
        return self.cursor.fetchall()

    def search_courses(self, keyword):
        """5. 关键词模糊搜索课程"""
        query = """
            SELECT code, name, credit, hours, type
            FROM course
            WHERE name LIKE ? OR code LIKE ?
            LIMIT 30
        """
        self.cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
        return self.cursor.fetchall()

    def get_college_majors(self, college_name):
        """6. 查询某学院下所有专业"""
        query = """
            SELECT m.name, m.total_credits
            FROM major m
            WHERE m.college LIKE ?
        """
        self.cursor.execute(query, (f'%{college_name}%',))
        return self.cursor.fetchall()

    def cross_university_compare(self, major_name, univ1, univ2):
        """7. 跨校对比"""
        query = """
            SELECT u.name, m.name, m.total_credits
            FROM major m
            JOIN university u ON m.univ_id = u.id
            WHERE m.name LIKE ? AND u.name LIKE ? OR u.name LIKE ?
        """
        self.cursor.execute(query, (f'%{major_name}%', f'%{univ1}%', f'%{univ2}%'))
        return self.cursor.fetchall()


class NLQueryParser:
    """自然语言查询解析器"""

    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.patterns = [
            {
                'name': '查询专业必修课',
                'pattern': r'(?:查询|查看|列出)?\s*([^\d\W]{2,15})\s*专业(?:的)?\s*必修课',
                'sql': """
                    SELECT c.code, c.name, c.credit, c.hours
                    FROM course c
                    JOIN program_course pc ON c.id = pc.course_id
                    JOIN major m ON pc.major_id = m.id
                    WHERE m.name LIKE '%{}%' AND pc.is_required = 1
                    LIMIT 20
                """,
                'headers': ['课程代码', '课程名称', '学分', '学时']
            },
            {
                'name': '查询课程学分',
                'pattern': r'《?([^》]{2,20})》?\s*(?:课程|课)?\s*(?:的)?\s*学分',
                'sql': """
                    SELECT c.code, c.name, c.credit, c.hours
                    FROM course c
                    WHERE c.name LIKE '%{}%'
                    LIMIT 10
                """,
                'headers': ['课程代码', '课程名称', '学分', '学时']
            },
            {
                'name': '查询专业总学分',
                'pattern': r'([^\d\W]{2,15})\s*专业\s*(?:的)?\s*总学分',
                'sql': """
                    SELECT m.name, m.total_credits
                    FROM major m
                    WHERE m.name LIKE '%{}%'
                """,
                'headers': ['专业名称', '总学分']
            },
            {
                'name': '搜索课程',
                'pattern': r'(?:搜索|查找|找)\s*([^ ]{2,20})\s*(?:课程|课)',
                'sql': """
                    SELECT c.code, c.name, c.credit, c.hours
                    FROM course c
                    WHERE c.name LIKE '%{}%'
                    LIMIT 20
                """,
                'headers': ['课程代码', '课程名称', '学分', '学时']
            },
            {
                'name': '跨校对比',
                'pattern': r'(?:比较|对比)\s*([^\d\W]{2,15})\s*专业\s*在\s*([^\d\W]{2,20})\s*和\s*([^\d\W]{2,20})\s*的学分',
                'sql': """
                    SELECT u.name, m.name, m.total_credits
                    FROM major m
                    JOIN university u ON m.univ_id = u.id
                    WHERE m.name LIKE '%{}%' AND u.name LIKE '%{}%' OR u.name LIKE '%{}%'
                """,
                'headers': ['大学', '专业', '总学分']
            }
        ]

    def parse(self, question):
        """解析自然语言问题"""
        for pattern_info in self.patterns:
            match = re.search(pattern_info['pattern'], question)
            if match:
                print(f"\n🔍 识别到查询类型: {pattern_info['name']}")
                sql = pattern_info['sql'].format(*match.groups())
                print(f"📝 执行SQL: {sql}")
                try:
                    self.cursor.execute(sql)
                    results = self.cursor.fetchall()
                    return self._format_results(results, pattern_info['headers'])
                except Exception as e:
                    return f"❌ 查询执行失败: {e}"

        return "❌ 无法识别您的问题。\n请尝试：\n  • '计算机科学与技术专业必修课'\n  • '数据结构课程的学分'\n  • '计算机科学与技术专业总学分'\n  • '搜索数据库课程'\n  • '对比计算机科学与技术专业在西南财经大学和上海财经大学的学分'"

    def _format_results(self, results, headers):
        if not results:
            return "未找到相关数据"

        table = PrettyTable()
        table.field_names = headers
        for row in results:
            formatted_row = []
            for item in row:
                if item is None:
                    formatted_row.append('-')
                else:
                    formatted_row.append(str(item)[:50])
            table.add_row(formatted_row)
        return str(table)

    def close(self):
        self.conn.close()


def print_banner():
    """打印系统横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║                     🌟 培养方案数据库系统 v1.0 🌟                            ║
    ║                    Curriculum Database System                                ║
    ║                                                                              ║
    ║              西南财经大学 - 计算机与人工智能学院                              ║
    ║                                                                              ║
    ║              支持自然语言查询 | 跨校对比分析                                  ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """打印主菜单"""
    print("\n" + "=" * 60)
    print("📌 请选择功能：")
    print("=" * 60)
    print("  1. 📚 查询专业必修课列表")
    print("  2. 🔍 查询课程学分、学时信息")
    print("  3. 📊 查询专业总学分要求")
    print("  4. 🏫 查询开设某课程的所有专业")
    print("  5. 🔎 关键词模糊搜索课程")
    print("  6. 💬 自然语言查询（智能问答）")
    print("  7. 🌐 跨校对比分析")
    print("  0. 🚪 退出系统")
    print("=" * 60)


def query_required_courses(q):
    """功能1：查询专业必修课"""
    print("\n--- 📚 查询专业必修课 ---")
    major = input("请输入专业名称（如：计算机科学与技术）: ").strip()
    if not major:
        print("❌ 专业名称不能为空")
        return

    results = q.get_required_courses(major)

    if results:
        table = PrettyTable()
        table.field_names = ["课程代码", "课程名称", "学分", "学时"]
        for row in results[:30]:
            name = row[1][:45] + "..." if len(str(row[1])) > 45 else row[1]
            table.add_row([row[0], name, row[2], row[3]])
        print(table)
        print(f"\n✅ 共 {len(results)} 门必修课")
    else:
        print(f"❌ 未找到专业 '{major}' 的必修课信息")


def query_course_info(q):
    """功能2：查询课程信息"""
    print("\n--- 🔍 查询课程信息 ---")
    course_name = input("请输入课程名称（支持模糊搜索）: ").strip()
    if not course_name:
        print("❌ 课程名称不能为空")
        return

    results = q.get_course_info(course_name)

    if results:
        table = PrettyTable()
        table.field_names = ["课程代码", "课程名称", "学分", "学时", "类型"]
        for row in results:
            name = row[1][:40] + "..." if len(str(row[1])) > 40 else row[1]
            table.add_row([row[0], name, row[2], row[3], row[4]])
        print(table)
    else:
        print(f"❌ 未找到课程 '{course_name}' 的信息")


def query_major_credits(q):
    """功能3：查询专业总学分"""
    print("\n--- 📊 查询专业总学分 ---")
    major = input("请输入专业名称: ").strip()
    if not major:
        print("❌ 专业名称不能为空")
        return

    result = q.get_major_total_credits(major)

    if result:
        print(f"\n✅ 专业: {result[0]}")
        print(f"✅ 总学分要求: {result[1]} 学分")
    else:
        print(f"❌ 未找到专业 '{major}' 的信息")


def query_majors_by_course(q):
    """功能4：查询开设某课程的专业"""
    print("\n--- 🏫 查询开设某课程的专业 ---")
    course_name = input("请输入课程名称: ").strip()
    if not course_name:
        print("❌ 课程名称不能为空")
        return

    results = q.get_majors_by_course(course_name)

    if results:
        table = PrettyTable()
        table.field_names = ["专业名称", "所属大学"]
        for row in results:
            table.add_row([row[0], row[1]])
        print(table)
    else:
        print(f"❌ 未找到开设 '{course_name}' 课程的专业")


def search_courses(q):
    """功能5：关键词搜索"""
    print("\n--- 🔎 关键词搜索课程 ---")
    keyword = input("请输入搜索关键词: ").strip()
    if not keyword:
        print("❌ 关键词不能为空")
        return

    results = q.search_courses(keyword)

    if results:
        table = PrettyTable()
        table.field_names = ["课程代码", "课程名称", "学分", "学时", "类型"]
        for row in results:
            name = row[1][:40] + "..." if len(str(row[1])) > 40 else row[1]
            table.add_row([row[0], name, row[2], row[3], row[4]])
        print(table)
        print(f"\n✅ 共找到 {len(results)} 门相关课程")
    else:
        print(f"❌ 未找到与 '{keyword}' 相关的课程")


def natural_language_query(parser):
    """功能6：自然语言查询"""
    print("\n--- 💬 自然语言查询（智能问答）---")
    print("📖 支持的问题示例：")
    print("  • '计算机科学与技术专业必修课'")
    print("  • '数据结构课程的学分'")
    print("  • '计算机科学与技术专业总学分'")
    print("  • '搜索数据库课程'")
    print("  • '对比金融学专业在西南财经大学和上海财经大学的学分'")
    print("-" * 50)

    question = input("💬 请输入您的问题: ").strip()
    if not question:
        print("❌ 问题不能为空")
        return

    result = parser.parse(question)
    print("\n" + "=" * 50)
    print("📊 查询结果:")
    print("=" * 50)
    print(result)


def cross_compare(q):
    """功能7：跨校对比"""
    print("\n--- 🌐 跨校对比分析 ---")
    major = input("请输入专业名称（如：金融学）: ").strip()
    univ1 = input("请输入第一所大学（如：西南财经大学）: ").strip()
    univ2 = input("请输入第二所大学（如：上海财经大学）: ").strip()

    if not all([major, univ1, univ2]):
        print("❌ 所有字段都不能为空")
        return

    results = q.cross_university_compare(major, univ1, univ2)

    if results:
        table = PrettyTable()
        table.field_names = ["大学名称", "专业名称", "总学分"]
        for row in results:
            table.add_row([row[0], row[1], row[2]])
        print(table)

        if len(results) == 2:
            diff = abs(results[0][2] - results[1][2])
            print(f"\n📊 学分差异: {diff} 学分")
    else:
        print(f"❌ 未找到对比数据")


def main():
    """主程序"""
    print_banner()

    # 检查数据库是否存在
    import os
    if not os.path.exists(DB_PATH):
        print("⚠️  数据库不存在！请先运行以下命令创建数据库：")
        print("   1. python init_db.py")
        print("   2. python import_data.py")
        print("\n程序退出。")
        return

    q = CurriculumQuery()
    parser = NLQueryParser()

    while True:
        print_menu()
        choice = input("\n👉 请输入选项（0-7）: ").strip()

        if choice == '0':
            print("\n👋 感谢使用，再见！")
            q.close()
            parser.close()
            sys.exit(0)
        elif choice == '1':
            query_required_courses(q)
        elif choice == '2':
            query_course_info(q)
        elif choice == '3':
            query_major_credits(q)
        elif choice == '4':
            query_majors_by_course(q)
        elif choice == '5':
            search_courses(q)
        elif choice == '6':
            natural_language_query(parser)
        elif choice == '7':
            cross_compare(q)
        else:
            print("❌ 无效选项，请输入 0-7 之间的数字")

        input("\n按 Enter 键继续...")


if __name__ == "__main__":
    main()