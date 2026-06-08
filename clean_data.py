# clean_data.py
# clean_data.py（支持多专业版）
import pandas as pd
import re
from config import CSV_DIR
import os


def clean_course_data_for_major(csv_files, major_name):
    """清洗单个专业的课程数据"""
    all_courses = []

    for csv_file in csv_files:
        df = pd.read_csv(os.path.join(CSV_DIR, csv_file))

        if df.empty or len(df.columns) < 3:
            continue

        for _, row in df.iterrows():
            if len(row) < 3:
                continue

            code = row.iloc[0] if pd.notna(row.iloc[0]) else None
            name = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else None

            if not code or not name:
                continue

            # 跳过无效行
            skip_keywords = ['合计', 'In Total', '培养目标', '毕业要求', '模块', '比例']
            if any(keyword in str(name) for keyword in skip_keywords):
                continue

            # 跳过包含百分比的行
            if '%' in str(code) or '%' in str(name):
                continue

            code = str(code).replace('\n', '').strip()
            name = str(name).replace('\n', ' ').strip()

            # 跳过过短或无效的代码
            if len(code) < 3 or code.isdigit():
                continue

            # 提取学分
            credit = None
            for i in range(2, min(5, len(row))):
                credit = extract_credit(row.iloc[i])
                if credit is not None:
                    break

            # 过滤异常学分
            if credit is not None and (credit > 10 or credit < 0.5):
                continue

            if credit is None or credit <= 0:
                continue

            # 提取学时
            hours = 0
            for i in range(4, min(7, len(row))):
                h = extract_hours(row.iloc[i])
                if h is not None:
                    hours = h
                    break

            # 课程类型
            course_type = '必修'
            for i in range(7, min(10, len(row))):
                if i < len(row) and pd.notna(row.iloc[i]):
                    if '选修' in str(row.iloc[i]):
                        course_type = '选修'
                        break

            all_courses.append({
                'code': code,
                'name': name,
                'credit': credit,
                'hours': hours,
                'type': course_type,
                'major': major_name
            })

    # 去重
    seen = set()
    unique = []
    for c in all_courses:
        if c['code'] not in seen:
            seen.add(c['code'])
            unique.append(c)

    return pd.DataFrame(unique)


def extract_credit(value):
    if pd.isna(value):
        return None
    val_str = str(value).strip()
    if '%' in val_str or '％' in val_str:
        return None
    match = re.search(r'(\d+(?:\.\d+)?)', val_str)
    if match:
        num = float(match.group(1))
        if 0.5 <= num <= 10:
            return num
    return None


def extract_hours(value):
    if pd.isna(value):
        return None
    match = re.search(r'(\d+)', str(value))
    if match:
        num = int(match.group(1))
        if 1 <= num <= 200:
            return num
    return None


def process_all_majors():
    """处理所有专业的CSV文件"""

    # 获取所有原始表格文件，按专业分组
    csv_files = [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]

    # 分组
    major_groups = {}
    for f in csv_files:
        # 提取专业标识（PDF文件名部分）
        if '_table_' in f:
            major_key = f.split('_table_')[0]
            if major_key not in major_groups:
                major_groups[major_key] = []
            major_groups[major_key].append(f)

    print(f"找到 {len(major_groups)} 个专业的表格\n")

    all_majors_data = []

    for major_key, files in major_groups.items():
        print(f"正在处理专业: {major_key}")
        print(f"  表格文件数: {len(files)}")

        # 按表格序号排序
        files_sorted = sorted(files, key=lambda x: int(x.split('_table_')[1].split('.')[0]))

        # 清洗数据
        cleaned_df = clean_course_data_for_major(files_sorted, major_key)

        # 保存
        output_path = os.path.join(CSV_DIR, f"{major_key}_cleaned.csv")
        cleaned_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"  ✅ 保存 {len(cleaned_df)} 门课程")

        all_majors_data.append(cleaned_df)
        print()

    # 合并所有专业数据
    if all_majors_data:
        combined_df = pd.concat(all_majors_data, ignore_index=True)
        combined_path = os.path.join(CSV_DIR, "all_courses_cleaned.csv")
        combined_df.to_csv(combined_path, index=False, encoding='utf-8-sig')
        print(f"✅ 合并保存: {len(combined_df)} 门课程（所有专业）")


if __name__ == "__main__":
    process_all_majors()