from sqlalchemy import text
from config import db, app

table_name = "books"
table2_name = "refs"

def table_exists(name):
    sql_table_existence = text(
		"  SELECT EXISTS (  "
		"  SELECT 1  "
		"  FROM information_schema.tables  "
		f" WHERE table_name = '{name}'"
		"  )  "
	)
    print(f"Checking if table {name} exists")
    print(sql_table_existence)
    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]

def reset_db():
    print(f"Clearing contents from table {table_name}")
    sql = text(f"DELETE FROM {table_name}")
    db.session.execute(sql)
    db.session.commit()

def setup_db():
    if table_exists(table_name):
        print(f"Table {table_name} exists, dropping")
        sql = text(f"DROP TABLE {table_name}")
        db.session.execute(sql)
        db.session.commit()

    print(f"Creating table {table_name}")
    sql = text(
        f" CREATE TABLE {table_name} ("
        " id SERIAL PRIMARY KEY, "
        " key TEXT NOT NULL, "
        " author TEXT NOT NULL, "
        " year INTEGER NOT NULL, "
        " title TEXT NOT NULL, "
        " publisher TEXT NOT NULL, "
        " address TEXT, "
        " volume TEXT, "
        " series TEXT, "
        " edition TEXT, "
        " month TEXT, "
        " note TEXT, "
        " url TEXT "
        ");"
	)

    db.session.execute(sql)
    db.session.commit()

def references_table_exists():
    sql_table_existence = text(
        "SELECT EXISTS ( "
        "  SELECT 1 "
        "  FROM information_schema.tables "
        f" WHERE table_name = '{table2_name}'"
        ")"
    )
    print(f"Checking if table {table2_name} exists")
    result = db.session.execute(sql_table_existence)
    return result.fetchall()[0][0]

def reset_references_table():
    print(f"Clearing contents from table {table2_name}")
    sql = text(f"DELETE FROM {table2_name}")
    db.session.execute(sql)
    db.session.commit()

def setup_references_table():
    if references_table_exists():
        print(f"Table {table2_name} exists, dropping")
        sql = text(f"DROP TABLE {table2_name}")
        db.session.execute(sql)
        db.session.commit()

    print(f"Creating table {table2_name}")
    sql = text(
        f" CREATE TABLE IF NOT EXISTS {table2_name} ( "
        "id SERIAL PRIMARY KEY, "
        "entry_type VARCHAR(50) NOT NULL, "
        "citation_key VARCHAR(100) UNIQUE NOT NULL, "
        "author TEXT NOT NULL, "
        "title TEXT NOT NULL, "
        "year VARCHAR(4) NOT NULL, "
        "tag VARCHAR(50), "
        "bibtex TEXT NOT NULL "
        ");"
    )
    db.session.execute(sql)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        setup_db()
        setup_references_table()
