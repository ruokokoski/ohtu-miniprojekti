from config import db
from sqlalchemy import text
#from entities.reference import Reference

def get_references():
    pass
    #sql_query = text("SELECT...")
    #result = db.session.execute(sql_query)
    #references = result.fetchall()
    #return

def list_references(): # need to create the database first
    pass
    #sql = text('SELECT author, title FROM "references" ORDER BY author DESC')
    #result = db.session.execute(sql).fetchall()
    #return result



'''
def create_reference(content):
    pass
    sql_query = text("INSERT...")
    db.session.execute(sql_query, { "content": content })
    db.session.commit()
'''
