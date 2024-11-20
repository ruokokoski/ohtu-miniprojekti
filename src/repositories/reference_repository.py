from sqlalchemy import text
from config import db

def list_references():
    sql = text('SELECT author, year, title, publisher, address, key '
        ' FROM books '
        'ORDER BY key')
    result = db.session.execute(sql).fetchall()
    return result

def create_reference(data):

    columns = ', '.join(data.keys()) # (col1, col2...)
    placeholders = ', '.join(f":{key}" for key in data.keys()) # (:col1, :col2...)

    sql_query = text(f"""INSERT INTO Books ({columns}) VALUES ({placeholders})""")

    db.session.execute(sql_query, data)
    db.session.commit()

#bibtex-haun testaus refs-taulusta:
def get_bibtex():
    sql = text('SELECT bibtex FROM refs;')
    result = db.session.execute(sql).fetchall()
    return result
