from ...db import get_db

def addCollege(college):
  db = get_db()
  mycursor = db.cursor()

  sql = "INSERT INTO college(college_code, college_name) VALUES (%s, %s)"
  mycursor.execute(sql, college)
  db.commit()

  mycursor.close()