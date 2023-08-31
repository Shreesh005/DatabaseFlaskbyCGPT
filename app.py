from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_input (
            id INTEGER PRIMARY KEY,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_data = request.form['data']
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_input (data) VALUES (?)', (user_data,))
        conn.commit()
        conn.close()
    return render_template('index.html')

@app.route('/download_db', methods=['GET'])
def download_db():
    # Set appropriate headers to trigger download
    response = app.response_class(
        open('data.db', 'rb').read(),
        mimetype='application/x-sqlite3',
        headers={'Content-Disposition': 'attachment; filename=data.db'}
    )
    return response



if __name__ == '__main__':
    create_table()  # Create the table before running the app
    app.run(debug=True)
