# web_app.py（修复版 - 不使用 format 处理 CSS）
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import sqlite3
from config import DB_PATH

app = FastAPI(title="培养方案数据库系统")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>培养方案数据库系统</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 50px; }
        .header h1 { font-size: 36px; color: white; margin-bottom: 10px; }
        .header p { font-size: 16px; color: rgba(255,255,255,0.9); }
        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 30px;
            font-size: 14px;
            color: white;
            margin-top: 15px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .card:hover { transform: translateY(-5px); }
        .card-icon { font-size: 32px; margin-bottom: 15px; }
        .card h3 { color: #333; margin-bottom: 15px; font-size: 18px; }
        .card p { color: #666; font-size: 13px; margin-bottom: 20px; }
        input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 14px;
            margin-bottom: 15px;
        }
        input:focus { outline: none; border-color: #667eea; }
        button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            border: none;
            border-radius: 12px;
            font-size: 15px;
            cursor: pointer;
        }
        button:hover { opacity: 0.9; }
        .example { font-size: 12px; color: #999; margin-top: 10px; text-align: center; }
        footer { text-align: center; color: rgba(255,255,255,0.7); font-size: 13px; margin-top: 40px; }
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 28px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 培养方案数据库系统</h1>
            <p>Curriculum Database System</p>
            <div class="badge">西南财经大学 · 计算机与人工智能学院</div>
        </div>

        <div class="grid">
            <div class="card">
                <div class="card-icon">📖</div>
                <h3>1. 查询专业必修课列表</h3>
                <p>查看指定专业的全部必修课程</p>
                <form action="/query1" method="post">
                    <input type="text" name="major" placeholder="例：金融学、计算机科学与技术" required>
                    <button type="submit">查询必修课</button>
                </form>
                <div class="example">💡 支持模糊搜索</div>
            </div>

            <div class="card">
                <div class="card-icon">🔍</div>
                <h3>2. 查询课程学分学时信息</h3>
                <p>获取课程的学分、学时、类型详情</p>
                <form action="/query2" method="post">
                    <input type="text" name="course" placeholder="例：高等数学、数据结构" required>
                    <button type="submit">查询课程</button>
                </form>
                <div class="example">💡 支持模糊搜索</div>
            </div>

            <div class="card">
                <div class="card-icon">📊</div>
                <h3>3. 查询专业总学分要求</h3>
                <p>查看专业毕业所需总学分</p>
                <form action="/query3" method="post">
                    <input type="text" name="major" placeholder="例：金融学、计算机科学与技术" required>
                    <button type="submit">查询总学分</button>
                </form>
                <div class="example">💡 精确查询专业名称</div>
            </div>

            <div class="card">
                <div class="card-icon">🏫</div>
                <h3>4. 查询开设某课程的所有专业</h3>
                <p>查看哪些专业开设了该课程</p>
                <form action="/query4" method="post">
                    <input type="text" name="course" placeholder="例：高等数学、微观经济学" required>
                    <button type="submit">查询专业</button>
                </form>
                <div class="example">💡 支持模糊搜索</div>
            </div>

            <div class="card">
                <div class="card-icon">🎓</div>
                <h3>5. 查询某学院下所有专业</h3>
                <p>查看学院下属专业及课程数量</p>
                <form action="/query5" method="post">
                    <input type="text" name="college" placeholder="例：计算机、金融、会计" required>
                    <button type="submit">查询专业</button>
                </form>
                <div class="example">💡 支持模糊搜索</div>
            </div>

            <div class="card">
                <div class="card-icon">🔎</div>
                <h3>6. 关键词模糊搜索课程</h3>
                <p>通过关键词快速查找课程</p>
                <form action="/query6" method="post">
                    <input type="text" name="keyword" placeholder="例：金融、计算机、数学" required>
                    <button type="submit">搜索课程</button>
                </form>
                <div class="example">💡 支持课程代码和名称搜索</div>
            </div>
        </div>

        <footer>© 2025 培养方案数据库系统 | 支持6类查询 | 跨校对比分析功能已就绪</footer>
    </div>
</body>
</html>
"""


# 结果页面生成函数（不使用 format 处理 CSS）
def generate_result_page(title, count, table_html):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>查询结果</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .back-btn {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 10px 24px;
            border-radius: 30px;
            text-decoration: none;
            margin-bottom: 20px;
        }}
        .result-card {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }}
        .result-title {{ font-size: 24px; color: #333; margin-bottom: 10px; padding-bottom: 15px; border-bottom: 3px solid #667eea; }}
        .stats {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 40px;
            display: inline-block;
            margin: 20px 0;
            font-size: 14px;
        }}
        .table-wrapper {{ overflow-x: auto; border-radius: 12px; border: 1px solid #e0e0e0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th {{ background: #f8f9fa; color: #333; padding: 14px 12px; text-align: left; border-bottom: 2px solid #e0e0e0; }}
        td {{ padding: 12px; border-bottom: 1px solid #f0f0f0; color: #555; }}
        tr:hover {{ background: #f8f9fa; }}
        .error {{ text-align: center; padding: 40px; color: #e74c3c; font-size: 16px; }}
        footer {{ text-align: center; margin-top: 20px; color: rgba(255,255,255,0.7); font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-btn">← 返回首页</a>
        <div class="result-card">
            <h2 class="result-title">{title}</h2>
            <div class="stats">📊 共找到 {count} 条记录</div>
            <div class="table-wrapper">{table_html}</div>
        </div>
        <footer>© 2025 培养方案数据库系统</footer>
    </div>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(HOME_PAGE)


# 功能1：必修课列表
@app.post("/query1", response_class=HTMLResponse)
async def query1(major: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.code, c.name, c.credit, c.hours
        FROM course c
        JOIN program_course pc ON c.id = pc.course_id
        JOIN major m ON pc.major_id = m.id
        WHERE m.name LIKE ? AND pc.is_required = 1
        ORDER BY c.code
    """, (f'%{major}%',))
    results = cursor.fetchall()
    conn.close()

    if results:
        html = '<table><thead><tr><th>课程代码</th><th>课程名称</th><th>学分</th><th>学时</th></tr></thead><tbody>'
        for row in results:
            html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>'
        html += '</tbody></table>'
    else:
        html = '<div class="error">未找到相关课程</div>'

    return HTMLResponse(generate_result_page(f"《{major}》专业必修课列表", len(results), html))


# 功能2：课程信息
@app.post("/query2", response_class=HTMLResponse)
async def query2(course: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT code, name, credit, hours, type
        FROM course
        WHERE name LIKE ?
        ORDER BY code
    """, (f'%{course}%',))
    results = cursor.fetchall()
    conn.close()

    if results:
        html = '<table><thead><tr><th>课程代码</th><th>课程名称</th><th>学分</th><th>学时</th><th>类型</th></tr></thead><tbody>'
        for row in results:
            html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>'
        html += '</tbody></table>'
    else:
        html = '<div class="error">未找到相关课程</div>'

    return HTMLResponse(generate_result_page(f"《{course}》课程信息", len(results), html))


# 功能3：专业总学分
@app.post("/query3", response_class=HTMLResponse)
async def query3(major: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, college, total_credits
        FROM major
        WHERE name LIKE ?
    """, (f'%{major}%',))
    results = cursor.fetchall()
    conn.close()

    if results:
        html = '<table><thead><tr><th>专业名称</th><th>所属学院</th><th>总学分</th></tr></thead><tbody>'
        for row in results:
            html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]} 学分</td></tr>'
        html += '</tbody></table>'
    else:
        html = '<div class="error">未找到相关专业</div>'

    return HTMLResponse(generate_result_page(f"《{major}》专业学分要求", len(results), html))


# 功能4：开设课程的专业
@app.post("/query4", response_class=HTMLResponse)
async def query4(course: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT m.name, m.college
        FROM major m
        JOIN program_course pc ON m.id = pc.major_id
        JOIN course c ON pc.course_id = c.id
        WHERE c.name LIKE ?
        ORDER BY m.name
    """, (f'%{course}%',))
    results = cursor.fetchall()
    conn.close()

    if results:
        html = '<table><thead><tr><th>专业名称</th><th>所属学院</th></tr></thead><tbody>'
        for row in results:
            html += f'<tr><td>{row[0]}</td><td>{row[1]}</td></tr>'
        html += '</tbody></table>'
    else:
        html = '<div class="error">未找到开设该课程的专业</div>'

    return HTMLResponse(generate_result_page(f"开设《{course}》课程的专业", len(results), html))


# 功能5：学院专业
@app.post("/query5", response_class=HTMLResponse)
async def query5(college: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name, m.college, m.total_credits, COUNT(pc.course_id) as course_count
        FROM major m
        LEFT JOIN program_course pc ON m.id = pc.major_id
        WHERE m.college LIKE ?
        GROUP BY m.id
        ORDER BY m.name
    """, (f'%{college}%',))
    results = cursor.fetchall()
    conn.close()

    if results:
        html = '<table><thead><tr><th>专业名称</th><th>所属学院</th><th>总学分</th><th>课程数量</th></tr></thead><tbody>'
        for row in results:
            html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]} 学分</td><td>{row[3]} 门</td></tr>'
        html += '</tbody></table>'
    else:
        html = '<div class="error">未找到该学院的专业</div>'

    return HTMLResponse(generate_result_page(f"《{college}》学院专业一览", len(results), html))


# 功能6：关键词搜索
@app.post("/query6", response_class=HTMLResponse)
async def query6(keyword: str = Form(...)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT code, name, credit, hours, type
        FROM course
        WHERE name LIKE ? OR code LIKE ?
        ORDER BY name
    """, (f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    conn.close()

    if results:
        html = '<table><thead><tr><th>课程代码</th><th>课程名称</th><th>学分</th><th>学时</th><th>类型</th></tr></thead><tbody>'
        for row in results:
            html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>'
        html += '</tbody></table>'
    else:
        html = '<div class="error">未找到相关课程</div>'

    return HTMLResponse(generate_result_page(f"关键词「{keyword}」搜索结果", len(results), html))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)