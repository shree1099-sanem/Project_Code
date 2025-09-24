from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ganesha@123'  
app.config['MYSQL_DB'] = 'Marketplace'

mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, description FROM jobs ORDER BY created_at DESC LIMIT 10")
    recent_jobs = cur.fetchall()

    cur.execute("""
        SELECT jobs.id, jobs.description, COUNT(bids.id)
        FROM jobs
        LEFT JOIN bids ON jobs.id = bids.jobs_id
        WHERE jobs.expires_at > NOW()
        GROUP BY jobs.id
        ORDER BY COUNT(bids.id) DESC
        LIMIT 10
    """)
    top_active_jobs = cur.fetchall()
    cur.close()

    return render_template('home.html', recent_jobs=recent_jobs, top_active_jobs=top_active_jobs)

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        description = request.form['description']
        requirements = request.form['requirements']
        expires_at = request.form['expires_at']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posters (name, contact_info) VALUES (%s, %s)", (name, contact))
        poster_id = cur.lastrowid
        cur.execute("""
            INSERT INTO jobs (poster_id, description, requirements, created_at, expires_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (poster_id, description, requirements, datetime.now(), expires_at))
        mysql.connection.commit()
        cur.close()

        return redirect('/')
    return render_template('job_posting.html')

@app.route('/job/<int:job_id>', methods=['GET', 'POST'])
def job_detail(job_id):
    cur = mysql.connection.cursor()

    # Fetch job info
    cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    job = cur.fetchone()

    if not job:
        cur.close()
        return "Job not found", 404

    # Handle bid submission
    if request.method == 'POST':
        bidder_name = request.form['bidder_name'].strip()
        amount = request.form['amount']

        if bidder_name and amount and float(amount) > 0:
            cur.execute("""
                INSERT INTO bids (job_id, bidder_name, amount, created_at)
                VALUES (%s, %s, %s, %s)
            """, (job_id, bidder_name, amount, datetime.now()))
            mysql.connection.commit()

    # Fetch bids sorted by amount
    cur.execute("""
        SELECT * FROM bids
        WHERE jobs_id = %s
        ORDER BY amount ASC
    """, (job_id,))
    bids = cur.fetchall()
    cur.close()

    return render_template('job_detail.html', job=job, bids=bids)

if __name__ == '__main__':
    app.run(debug=True)