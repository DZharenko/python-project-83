# models.py
from datetime import datetime
from urllib.parse import urlparse

import psycopg2
import requests
import validators
from flask import flash
from html_parser import html_parser
from psycopg2.extras import RealDictCursor


def get_db_connection(cursor_factory=None):
    
    import os

    from dotenv import load_dotenv
    load_dotenv()
    
    return psycopg2.connect(os.getenv('DATABASE_URL'),
                            cursor_factory=cursor_factory,
                            )


def normalize_url(url):
    
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def validate_url(url):
    
    if not url:
        return "URL обязателен"
    
    if len(url) > 255:
        return "URL не должен превышать 255 символов"
    
    if not validators.url(url):
        return "Некорректный URL"
    
    return None


def add_url(url):
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        normalized_url = normalize_url(url)
        
        cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
        existing_url = cur.fetchone()
        
        if existing_url:
            conn.rollback()
            flash('Страница уже существует', 'info')
            url_id = existing_url[0]
        else:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) "
                "RETURNING id",
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
    conn = get_db_connection(RealDictCursor)
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def get_all_urls(): 
    
    conn = get_db_connection(RealDictCursor)
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                u.id, 
                u.name, 
                u.created_at,
                (SELECT created_at 
                 FROM url_checks 
                 WHERE url_id = u.id 
                 ORDER BY created_at DESC 
                 LIMIT 1) as last_check,
                (SELECT status_code 
                 FROM url_checks 
                 WHERE url_id = u.id 
                 ORDER BY created_at DESC 
                 LIMIT 1) as status_code
            FROM urls u
            ORDER BY u.created_at DESC
        """)

        return cur.fetchall()   
    finally:
        cur.close()
        conn.close()


def add_url_check(id):

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT name FROM urls WHERE id = %s", (id,))
        url_result = cur.fetchone()

        if not url_result:
            raise Exception("URL не найден")

        url_name = url_result[0]

        try:
            response = requests.get(url_name, timeout=11)
            response.raise_for_status()

            status_code = response.status_code

            parsed_data = html_parser(url_name) if status_code == 200 else {}

            cur.execute(
                "INSERT INTO url_checks "
                "(url_id, status_code, h1, title, description) "
                "VALUES(%s, %s, %s, %s, %s) RETURNING id",
                (id, 
                 status_code,
                 parsed_data.get('h1'),
                 parsed_data.get('title'),
                 parsed_data.get('description')
                 )
                )
        except requests.RequestException:
            raise Exception("Ошибка при запросе к сайту")

        check_id = cur.fetchone()[0]
        conn.commit()
        return check_id
    
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
    

def get_url_checks(id):

    conn = get_db_connection(RealDictCursor)
    cur = conn.cursor()

    try:

        cur.execute(
            "SELECT * FROM url_checks WHERE url_id = %s "
            "ORDER BY created_at DESC",
            (id,)
        )
        return cur.fetchall()

    finally:
        cur.close()
        conn.close()

    

