# models.py
import psycopg2
from urllib.parse import urlparse
from datetime import datetime
import validators
from flask import flash

def get_db_connection():
    """Установка соединения с базой данных"""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def normalize_url(url):
    """Нормализация URL"""
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"

def validate_url(url):
    """Валидация URL"""
    if not url:
        return "URL обязателен"
    
    if len(url) > 255:
        return "URL не должен превышать 255 символов"
    
    if not validators.url(url):
        return "Некорректный URL"
    
    return None

def add_url(url):
    """Добавление URL в базу данных"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        normalized_url = normalize_url(url)
        
        # Проверяем существование URL
        cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
        existing_url = cur.fetchone()
        
        if existing_url:
            flash('Страница уже существует', 'info')
            url_id = existing_url[0]
        else:
            # Добавляем новый URL
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (normalized_url, datetime.now())
            )
            url_id = cur.fetchone()[0]
            conn.commit()
            flash('Страница успешно добавлена', 'success')
            
        return url_id
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_url_by_id(id):
    """Получение URL по ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

def get_all_urls():
    """Получение всех URL"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()