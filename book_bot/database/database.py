import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple

class Database:
    def __init__(self, db_path: str = 'database.db'):
        self.db_path = db_path
        self.init_tables()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    current_page INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица закладок
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    page_number INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            conn.commit()
    
    def get_user_page(self, user_id: int) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT current_page FROM users WHERE user_id = ?',
                (user_id,)
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                cursor.execute(
                    'INSERT INTO users (user_id) VALUES (?)',
                    (user_id,)
                )
                conn.commit()
                return 1
    
    def save_user_page(self, user_id: int, page: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT OR REPLACE INTO users (user_id, current_page) 
                   VALUES (?, ?)''',
                (user_id, page)
            )
            conn.commit()
    
    def add_bookmark(self, user_id: int, page: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Проверяем, есть ли уже такая закладка
            cursor.execute(
                '''SELECT id FROM bookmarks 
                   WHERE user_id = ? AND page_number = ?''',
                (user_id, page)
            )
            if cursor.fetchone():
                return False
            
            cursor.execute(
                '''INSERT INTO bookmarks (user_id, page_number) 
                   VALUES (?, ?)''',
                (user_id, page)
            )
            conn.commit()
            return True
    
    def get_bookmarks(self, user_id: int) -> List[Tuple[int, int]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT id, page_number FROM bookmarks 
                   WHERE user_id = ? ORDER BY page_number''',
                (user_id,)
            )
            return cursor.fetchall()
    
    def delete_bookmark(self, bookmark_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM bookmarks WHERE id = ?',
                (bookmark_id,)
            )
            conn.commit()
    
    def delete_all_bookmarks(self, user_id: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM bookmarks WHERE user_id = ?',
                (user_id,)
            )
            conn.commit()

db = Database()

async def init_db():
    db.init_tables()