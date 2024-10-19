import sys
import sqlite3
import shutil


if __name__ == '__main__':
    sql_file = sys.argv[1]
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    print(sql)

    db_path = r'C:\Users\63113\pantalone\db\pantalone.db'
    db_backup_path = r'C:\Users\63113\pantalone\db\pantalone.db.backup'

    shutil.copy(db_path, db_backup_path)
    print(f'Database backup to {db_backup_path}')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(sql)
    conn.commit()
