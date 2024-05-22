import sqlite3
import os

db_filename = 'data/data.db'

def initialize():
    if os.path.exists(db_filename):
        print('[INFO] Database already exists. Nothing to initialize.')
        return
    
    print('[INFO] Initializing database...')
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY NOT NULL,
            amount INTEGER NOT NULL,
            payment_method VARCHAR NOT NULL,
            timestamp DATE NOT NULL
        );
    ''')

    # Create manager table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manager (
            id INTEGER PRIMARY KEY NOT NULL,
            password VARCHAR NOT NULL
        );
    ''')

    cursor.execute('''
        INSERT INTO manager (id, password) VALUES (0, '0000');
    ''')
    conn.commit()

    conn.close()
    print('[INFO] Database initialized.')

