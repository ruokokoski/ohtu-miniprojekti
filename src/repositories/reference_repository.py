from config import db
from sqlalchemy import text
#from entities.reference import Reference

def get_references():
    pass
    #sql_query = text("SELECT...")
    #result = db.session.execute(sql_query)
    #references = result.fetchall()
    #return


def list_references():
    sql = text('SELECT author, year, title, publisher, address, key FROM books ORDER BY author DESC')
    result = db.session.execute(sql).fetchall()
    return result



'''
def create_reference(content):
    pass
    sql_query = text("INSERT...")
    db.session.execute(sql_query, { "content": content })
    db.session.commit()
'''
