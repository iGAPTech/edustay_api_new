import os
import mysql.connector
import sys

def setup_database():
    """Import database dump on first deployment"""
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()
        
        # Read and execute dump file
        with open('db/dump.sql', 'r') as f:
            sql_script = f.read()
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Database setup completed successfully")
    except Exception as e:
        print(f"⚠ Database setup skipped: {e}")
        # Don't fail deployment if DB already exists

if __name__ == '__main__':
    setup_database()