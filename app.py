from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'   # required for session management


# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# STUDENT FEEDBACK FORM (NO LOGIN)
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')



# -----------------------------
# SUBMIT FEEDBACK
# -----------------------------
@app.route('/submit', methods=['POST'])
def submit():
    subject = request.form['subject']
    faculty = request.form['faculty']
    rating = int(request.form['rating'])
    comment = request.form['comment']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO feedback (subject, faculty, rating, comment) VALUES (?, ?, ?, ?)',
        (subject, faculty, rating, comment)
    )
    conn.commit()
    conn.close()

    return redirect('/')


# -----------------------------
# ADMIN LOGIN
# -----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        admin = conn.execute(
            'SELECT * FROM admin WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()

        if admin:
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')


# -----------------------------
# ADMIN DASHBOARD (PROTECTED)
# -----------------------------
@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/login')

    conn = get_db_connection()

    # All feedback
    feedbacks = conn.execute('SELECT * FROM feedback').fetchall()

    # Overall statistics
    stats = conn.execute('''
        SELECT 
            COUNT(*) AS total,
            AVG(rating) AS average
        FROM feedback
    ''').fetchone()

    # Subject-wise analysis
    subject_stats = conn.execute('''
        SELECT subject, AVG(rating) AS avg_rating
        FROM feedback
        GROUP BY subject
    ''').fetchall()

    # Rating Distribution (1-5 stars)
    rating_counts = conn.execute('''
        SELECT rating, COUNT(*) as count 
        FROM feedback 
        GROUP BY rating
    ''').fetchall()
    
    # Process into a dictionary {1: count, 2: count...} to ensure all 5 stars exist
    rating_dist = {i: 0 for i in range(1, 6)}
    for r in rating_counts:
        rating_dist[int(r['rating'])] = r['count']

    conn.close()

    return render_template(
        'dashboard.html',
        feedbacks=feedbacks,
        total=stats['total'],
        average=round(stats['average'], 2) if stats['average'] else 0,
        subject_stats=subject_stats,
        rating_dist=rating_dist
    )


# -----------------------------
# DELETE FEEDBACK (ADMIN ONLY)
# -----------------------------
@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('admin'):
        return redirect('/login')

    conn = get_db_connection()
    conn.execute('DELETE FROM feedback WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect('/dashboard')


# -----------------------------
# LOGOUT
# -----------------------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')


# -----------------------------
# RUN APPLICATION
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
