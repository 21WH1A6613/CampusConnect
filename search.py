from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'dbname': 'campus_connect',
    'user': 'postgres',
    'password': 'indhu0504',
    'host': 'localhost',
    'port': '5432'
}

# Helper function to connect to the database
def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route("/search", methods=['GET', 'POST'])
def search_faculty():
    faculty_name = request.form.get('faculty_name')
    
    query = "SELECT name FROM faculty WHERE name ILIKE %s"
    params = [f"%{faculty_name}%"] if faculty_name else []

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute(query, params)
        results = cur.fetchall()

        cur.close()
        conn.close()

        if results:
            return jsonify([row['name'] for row in results])
        else:
            return jsonify({"message": "No faculty found"})
    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        return jsonify({"error": "Failed to fetch faculty"}), 500

if __name__ == "__main__":
    app.run(debug=True)
