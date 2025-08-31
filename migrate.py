import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def check_table_exists(cur, table_name):
    """Проверяет существование таблицы в базе данных"""
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = %s
        )
    """, (table_name,))
    return cur.fetchone()[0]

def print_table_structure(cur, table_name):
    """Выводит структуру таблицы"""
    cur.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = %s
        ORDER BY ordinal_position
    """, (table_name,))
    
    columns = cur.fetchall()
    print(f"\n📋 Структура таблицы '{table_name}':")
    for col in columns:
        null_info = "NULL" if col[2] == 'YES' else "NOT NULL"
        default_info = f" DEFAULT {col[3]}" if col[3] else ""
        print(f"  - {col[0]}: {col[1]} {null_info}{default_info}")

def apply_migrations():
    try:
        # Подключаемся к базе данных
        DATABASE_URL = os.getenv('DATABASE_URL')
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("🔍 Проверяем существование таблиц...")
        
        # Проверяем какие таблицы уже существуют
        urls_exists = check_table_exists(cur, 'urls')
        url_checks_exists = check_table_exists(cur, 'url_checks')
        
        print(f"📊 Состояние таблиц:")
        print(f"  - urls: {'✅ существует' if urls_exists else '❌ отсутствует'}")
        print(f"  - url_checks: {'✅ существует' if url_checks_exists else '❌ отсутствует'}")
        
        # Если обе таблицы уже существуют, пропускаем миграцию
        if urls_exists and url_checks_exists:
            print("✅ Все таблицы уже существуют, миграция не требуется")
            
            # Выводим структуру обеих таблиц
            print_table_structure(cur, 'urls')
            print_table_structure(cur, 'url_checks')
            
            cur.close()
            conn.close()
            return
        
        # Читаем SQL файл только если нужны миграции
        with open('database.sql', 'r') as f:
            sql_content = f.read()
        
        # Разделяем SQL команды по точкам с запятой
        sql_commands = sql_content.split(';')
        sql_commands = [cmd.strip() for cmd in sql_commands if cmd.strip()]
        
        print(f"🔧 Найдено {len(sql_commands)} SQL команд для выполнения")
        
        # Выполняем каждую команду отдельно
        for i, cmd in enumerate(sql_commands, 1):
            if cmd:
                try:
                    cur.execute(cmd)
                    print(f"✅ Команда {i} выполнена успешно")
                except Exception as cmd_error:
                    print(f"⚠️  Ошибка в команде {i}: {cmd_error}")
                    conn.rollback()
                    continue
        
        conn.commit()
        print("✅ Миграции успешно применены!")
        
        # Проверяем создание таблиц после миграции
        print("\n🔍 Проверяем результат миграции...")
        
        tables_to_check = ['urls', 'url_checks']
        for table_name in tables_to_check:
            exists = check_table_exists(cur, table_name)
            status = "✅ существует" if exists else "❌ отсутствует"
            print(f"  - {table_name}: {status}")
            
            if exists:
                print_table_structure(cur, table_name)
        
        # Показываем все таблицы в базе
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        all_tables = [table[0] for table in cur.fetchall()]
        print(f"\n📋 Все таблицы в базе: {', '.join(all_tables)}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка при применении миграций: {e}")
        if 'conn' in locals():
            conn.rollback()

if __name__ == "__main__":
    apply_migrations()