from MyCollege.db import get_db

def addCollege(college):
  db = get_db()
  mycursor = db.cursor()

  sql = "INSERT INTO college(college_code, college_name) VALUES (%s, %s)"
  mycursor.execute(sql, college)
  db.commit()

  mycursor.close()

def deleteCollege(college_code): 
  db = get_db()
  mycursor = db.cursor()

  sql = "DELETE FROM college WHERE college_code = %s"
  mycursor.execute(sql, college_code)
  db.commit()

  mycursor.close()
  
def editCollege(college):
  db = get_db()
  mycursor = db.cursor()

  sql = "UPDATE college SET college_code = %s, college_name = %s WHERE college_code = %s"
  mycursor.execute(sql , college)
  db.commit()

  mycursor.close()

def populateCollege(page):
  db = get_db()
  mycursor = db.cursor()

  offset = (page - 1) * 10
  sql = "SELECT * FROM college OFFSET %s LIMIT 10"
  mycursor.execute(sql, (offset,))
  result = mycursor.fetchall()

  return result

def getAllColleges(search='', start=0, length=10, order_column='college_code', order_dir='asc'):
  db = get_db()
  mycursor = db.cursor()
  order_dir = 'ASC' if order_dir.lower() == 'asc' else 'DESC'

  query = "SELECT * FROM college"
  params = []

  if search:
    query += " WHERE college_code ILIKE %s OR college_name ILIKE %s"
    params = [f'%{search}%', f'%{search}%']
  
  query += f" ORDER BY {order_column} {order_dir} OFFSET %s LIMIT %s"
  params.extend([start, length])

  mycursor.execute(query, params)
  result = mycursor.fetchall()
  mycursor.close()

  return result

def getCollegeCount(search=''):
  db = get_db()
  mycursor = db.cursor()

  if search:
    mycursor.execute("""
                     SELECT COUNT(*) FROM college 
                     WHERE college_code ILIKE %s OR college_name ILIKE %s
                     """, (f'%{search}%', f'%{search}%'))
  else:
    mycursor.execute("SELECT COUNT(*) FROM college")
  
  count = mycursor.fetchone()[0]
  mycursor.close()

  return count