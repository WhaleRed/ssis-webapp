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

def getAllColleges(search='', start=0, length=10):
  db = get_db()
  mycursor = db.cursor()

  if search:
    mycursor.execute("""
                     SELECT * FROM college 
                     WHERE college_code ILIKE %s OR college_name ILIKE %s 
                     ORDER BY college_code 
                     OFFSET %s LIMIT %s
                     """, (f'%{search}%', f'%{search}%', start, length))
  else: 
    mycursor.execute("""
                     Select * FROM college
                     ORDER BY college_code
                     OFFSET %s LIMIT %s
                     """, (start, length))
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