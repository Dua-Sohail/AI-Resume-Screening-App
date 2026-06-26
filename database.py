
from config import *
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

def insert_result(cv_name, score):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO results (cv_name, score) VALUES (%s, %s)"
    values = (cv_name, score)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

def fetch_results():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT cv_name, score FROM results")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def clear_results():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM results")
    conn.commit()
    cursor.close()
    conn.close()