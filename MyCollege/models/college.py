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