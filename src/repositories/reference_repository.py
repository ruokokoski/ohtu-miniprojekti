from sqlalchemy import text
from config import db
#from entities.reference import Reference

def list_references():
    sql = text('SELECT author, year, title, publisher, address, key '
        ' FROM books '
        'ORDER BY author DESC')
    result = db.session.execute(sql).fetchall()
    return result

'''
def create_reference(author, year, title, publisher, address, key):
    sql_query = text("INSERT...")
    db.session.execute(sql_query, {  })
    db.session.commit()
'''
