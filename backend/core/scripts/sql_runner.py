import sys
import sqlite3
import shutil

from src.libs.utils.path import get_db_path


if __name__ == "__main__":
    sql_file = sys.argv[1]
    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()
    print(sql)

    db_path = get_db_path()
    db_backup_path = f"{db_path}.bak"

    shutil.copy(db_path, db_backup_path)
    print(f"Database backup to {db_backup_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for s in sql.split(";"):
        if s:
            cursor.execute(s)
            conn.commit()
            res = cursor.fetchall()
            print(res)
