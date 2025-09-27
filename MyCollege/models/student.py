from ...db import get_db

def addStudent(student):
  db = get_db()
  mycursor = db.cursor()

  sql = "INSERT INTO student(student_id, first_name, last_name, year_level, gender, program_code) VALUES (%s, %s, %s, %s, %s, %s)"
  mycursor.execute(sql, student)
  db.commit()

  mycursor.close()

