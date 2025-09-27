from MyCollege.db import get_db

#functions take list as param

def addStudent(student):
  db = get_db()
  mycursor = db.cursor()

  sql = "INSERT INTO student(student_id, first_name, last_name, year_level, gender, program_code) VALUES (%s, %s, %s, %s, %s, %s)"
  mycursor.execute(sql, student)
  db.commit()

  mycursor.close()

def deleteStudent(idnum):           
  db = get_db()
  mycursor = db.cursor()

  sql = "DELETE FROM student WHERE student_id = %s"
  mycursor.execute(sql, idnum)
  db.commit()

  mycursor.close()

def editStudent(student):
  db = get_db()
  mycursor = db.cursor()

  sql = "UPDATE student SET student_id = %s, first_name = %s, last_name = %s, year_level = %s, gender = %s, program_code = %s WHERE student_id =%s"
  mycursor.execute(sql, student)
  db.commit()

  mycursor.close()