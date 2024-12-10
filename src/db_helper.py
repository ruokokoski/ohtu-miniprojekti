from sqlalchemy import text
from config import db, app

TABLE_NAME = "refs"

def reset_db():
    print(f"Clearing contents from table {TABLE_NAME}")
    sql = text(f"DELETE FROM {TABLE_NAME}")
    db.session.execute(sql)
    db.session.commit()

def references_table_exists():
    sql_table_existence = text(
        "SELECT EXISTS ( "
        "  SELECT 1 "
        "  FROM information_schema.tables "
        f" WHERE table_name = '{TABLE_NAME}'"
        ")"
    )
    print(f"Checking if table {TABLE_NAME} exists")
    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]

def setup_references_table():
    if references_table_exists():
        print(f"Table {TABLE_NAME} exists, dropping")
        sql = text(f"DROP TABLE {TABLE_NAME}")
        db.session.execute(sql)
        db.session.commit()

    print(f"Creating table {TABLE_NAME}")
    sql = text(
        f" CREATE TABLE IF NOT EXISTS {TABLE_NAME} ( "
        "id SERIAL PRIMARY KEY, "
        "entry_type TEXT NOT NULL, "
        "citation_key TEXT UNIQUE NOT NULL, "
        "author TEXT NOT NULL, "
        "title TEXT NOT NULL, "
        "year INTEGER NOT NULL, "
        "tag TEXT, "
        "extra_fields JSON NOT NULL "
        ");"
    )
    db.session.execute(sql)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        setup_references_table()
