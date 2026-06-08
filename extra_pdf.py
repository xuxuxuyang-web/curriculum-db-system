# extract_pdf.py
# extract_pdf.py（批量处理版）
import pdfplumber
import pandas as pd
from config import PDF_DIR, CSV_DIR
import os


def extract_tables_from_pdf(pdf_path):
    """从单个PDF中提取所有表格"""
    print(f"正在提取PDF: {os.path.basename(pdf_path)}")

    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        print(f"  PDF共 {len(pdf.pages)} 页")

        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if table and len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        if not df.empty:
                            all_tables.append(df)

    print(f"  共提取到 {len(all_tables)} 个表格")
    return all_tables


def save_raw_tables(tables, output_dir, pdf_name):
    """保存原始表格到CSV"""
    base_name = pdf_name.replace('.pdf', '')
    for i, table in enumerate(tables):
        csv_path = os.path.join(output_dir, f"{base_name}_table_{i + 1}.csv")
        table.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"  已保存 {len(tables)} 个CSV文件")


def process_all_pdfs():
    """批量处理所有PDF文件"""
    # 获取所有PDF文件
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]

    if not pdf_files:
        print(f"❌ 请先将PDF文件放到 {PDF_DIR} 文件夹中")
        return

    print(f"找到 {len(pdf_files)} 个PDF文件\n")

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        tables = extract_tables_from_pdf(pdf_path)
        save_raw_tables(tables, CSV_DIR, pdf_file)
        print()

    print(f"✅ 批量处理完成！共处理 {len(pdf_files)} 个PDF")


def extract_single_pdf(pdf_path):
    """处理单个PDF文件"""
    tables = extract_tables_from_pdf(pdf_path)
    pdf_name = os.path.basename(pdf_path)
    save_raw_tables(tables, CSV_DIR, pdf_name)
    return tables


if __name__ == "__main__":
    # 批量处理所有PDF
    process_all_pdfs()
