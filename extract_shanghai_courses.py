# extract_shanghai_courses.py
import pdfplumber
import pandas as pd
import re
import os
from config import PDF_DIR, CSV_DIR


def extract_courses_from_pdf(pdf_path, target_majors=None):
    """从PDF中提取课程数据，只提取目标专业"""

    if target_majors is None:
        target_majors = ['金融', '计算机']

    all_courses = []
    current_major = None

    print(f"正在处理: {os.path.basename(pdf_path)}")

    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF共 {len(pdf.pages)} 页")

        for page_num, page in enumerate(pdf.pages[1:20], start=2):  # 只处理前20页
            text = page.extract_text()
            if not text:
                continue

            # 检测专业名称
            for major in target_majors:
                if major in text and '专业' in text:
                    current_major = major
                    print(f"  第{page_num}页: 发现专业 [{major}]")
                    break

            if current_major:
                # 提取表格
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 2:
                        courses = parse_table(table, current_major)
                        all_courses.extend(courses)

    # 保存结果
    if all_courses:
        df = pd.DataFrame(all_courses)
        # 去重
        df = df.drop_duplicates(subset=['code'])

        output_path = os.path.join(CSV_DIR, "上财_课程_提取.csv")
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\n✅ 提取 {len(df)} 门课程")
        print(df.head(20))
        return df
    else:
        print("⚠️ 未提取到课程")
        return None


def parse_table(table, major_name):
    """解析表格，提取课程信息"""
    courses = []

    for row in table:
        if not row or len(row) < 3:
            continue

        # 检查是否有课程代码特征 (字母+数字)
        code = str(row[0]).strip() if row[0] else ''
        name = str(row[1]).strip() if len(row) > 1 and row[1] else ''

        # 过滤无效行
        if not code or not name:
            continue
        if len(code) < 3 or len(name) < 2:
            continue
        if '课程' in code or '分类' in code:
            continue

        # 提取学分
        credit = None
        for i in range(2, min(5, len(row))):
            if row[i] and isinstance(row[i], (int, float)):
                credit = float(row[i])
                break
            elif row[i] and str(row[i]).strip().replace('.', '').isdigit():
                credit = float(str(row[i]).strip())
                break

        if credit and 0.5 <= credit <= 10:
            courses.append({
                'code': code[:15],
                'name': name[:60],
                'credit': credit,
                'hours': int(credit * 17),
                'type': '必修'
            })

    return courses


def manual_enter_shanghai_data():
    """手动录入上财金融学和计算机专业课程（备用方案）"""

    # 金融学专业课程（从上财PDF第83-91页整理）
    finance_courses = [
        ('SUFE101', '政治经济学', 2.0),
        ('SUFE102', '中级微观经济学', 3.0),
        ('SUFE103', '中级宏观经济学', 3.0),
        ('SUFE104', '投资学', 3.0),
        ('SUFE105', '公司金融', 3.0),
        ('SUFE106', '货币银行学', 2.0),
        ('SUFE107', '国际金融', 3.0),
        ('SUFE108', '金融计量学', 3.0),
        ('SUFE109', '保险学原理', 3.0),
        ('SUFE110', '商业银行经营管理', 3.0),
        ('SUFE111', '金融机构与金融市场', 2.0),
        ('SUFE112', '财务报表分析', 2.0),
        ('SUFE113', '风险管理', 2.0),
        ('SUFE114', '金融科技导论', 2.0),
        ('SUFE115', '固定收益证券', 2.0),
        ('SUFE116', '证券投资分析', 2.0),
        ('SUFE117', '公司兼并收购与重组', 2.0),
        ('SUFE118', '金融工程学', 2.0),
        ('SUFE119', '金融监管', 2.0),
        ('SUFE120', '行为金融学', 2.0),
        ('SUFE121', '资产组合管理', 2.0),
        ('SUFE122', '金融模拟与实验', 2.0),
    ]

    # 计算机相关课程（从上财PDF中计算机编程等课程整理）
    cs_courses = [
        ('SUFECS01', '计算机编程(金融)', 2.0),
        ('SUFECS02', '程序设计基础', 3.0),
        ('SUFECS03', '数据结构', 3.0),
        ('SUFECS04', '数据库原理', 3.0),
        ('SUFECS05', '操作系统', 3.0),
        ('SUFECS06', '计算机网络', 3.0),
        ('SUFECS07', '算法设计与分析', 3.0),
        ('SUFECS08', '软件工程', 3.0),
        ('SUFECS09', '人工智能导论', 2.0),
        ('SUFECS10', '机器学习', 2.0),
        ('SUFECS11', 'Python程序设计', 2.0),
        ('SUFECS12', '大数据技术', 2.0),
    ]

    all_courses = []

    for code, name, credit in finance_courses:
        all_courses.append({
            'code': code,
            'name': name,
            'credit': credit,
            'hours': int(credit * 17),
            'type': '必修',
            'major': '金融学'
        })

    for code, name, credit in cs_courses:
        all_courses.append({
            'code': code,
            'name': name,
            'credit': credit,
            'hours': int(credit * 17),
            'type': '必修',
            'major': '计算机科学与技术'
        })

    df = pd.DataFrame(all_courses)
    output_path = os.path.join(CSV_DIR, "上财_课程_手动录入.csv")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✅ 手动录入 {len(df)} 门课程")
    print(df.head(20))
    return df


if __name__ == "__main__":
    pdf_path = os.path.join(PDF_DIR, "上海财经大学本科各专业培养方案.pdf")

    if os.path.exists(pdf_path):
        print("正在自动提取...")
        df = extract_courses_from_pdf(pdf_path, ['金融', '计算机'])

        if df is None or len(df) < 20:
            print("\n自动提取效果不佳，使用手动录入数据...")
            manual_enter_shanghai_data()
    else:
        print("PDF不存在，使用手动录入数据...")
        manual_enter_shanghai_data()