from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # زودنا عمود learn_skill عشان نسجل فيه المهارة المطلوبة للتعلم
    conn.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            learn_skill TEXT NOT NULL,
            owner TEXT NOT NULL
        )
    ''')
    
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM skills')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_skills = [
            ("Python Flask Web Development", "Programming", "Building scalable multi-page web applications utilizing MVC architectural pattern.", "Advanced JavaScript & React", "Yomna"),
            ("Data Structures & Algorithms (DSA)", "Computer Science", "Implementing efficient sorting algorithms, linked lists, and trees in Python.", "Machine Learning Basics", "Yomna"),
            ("Advanced Group Theory", "Mathematics", "Exploring algebraic structures, cyclic groups, and homomorphisms.", "Linear Algebra & Cryptography", "Ahmed"),
            ("UI/UX Modern Design Systems", "Design", "Designing wireframes and responsive layouts utilizing CSS Grid.", "Frontend Frameworks", "Sara")
        ]
        conn.executemany('''
            INSERT INTO skills (title, category, description, learn_skill, owner)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_skills)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    skills = conn.execute('SELECT * FROM skills ORDER BY id DESC LIMIT 3').fetchall()
    conn.close()
    return render_template('index.html', skills=skills)

@app.route('/skills')
def all_skills():
    conn = get_db_connection()
    skills = conn.execute('SELECT * FROM skills').fetchall()
    conn.close()
    return render_template('skills.html', skills=skills)

# إضافة مهارة جديدة (مع إضافة حقل المهارة المراد تعلمها)
@app.route('/add', methods=('GET', 'POST'))
def add_skill():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']
        learn_skill = request.form['learn_skill']
        owner = request.form['owner']

        conn = get_db_connection()
        conn.execute('INSERT INTO skills (title, category, description, learn_skill, owner) VALUES (?, ?, ?, ?, ?)',
                     (title, category, description, learn_skill, owner))
        conn.commit()
        conn.close()
        return redirect(url_for('all_skills'))

    return render_template('add_skill.html')

# صفحة تفاصيل المهارة (مع زر لطلب التبادل)
@app.route('/skill/<int:id>')
def skill_detail(id):
    conn = get_db_connection()
    skill = conn.execute('SELECT * FROM skills WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('skill_detail.html', skill=skill)

# مسار حذف مهارة
@app.route('/skill/delete/<int:id>', methods=('POST',))
def delete_skill(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM skills WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('all_skills'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)