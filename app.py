import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)

# MySQL config from environment
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Init MySQL
mysql = MySQL(app)

# Init Prometheus metrics
metrics = PrometheusMetrics(app)

# Custom counter: number of orders submitted
order_counter = Counter('order_submit_total', 'Total number of orders submitted')

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages ORDER BY id DESC')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    if new_message:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
        mysql.connection.commit()
        cur.close()
        order_counter.inc()  # Increment Prometheus metric
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
