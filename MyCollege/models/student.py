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

def populateStudent(page):
  db = get_db()
  mycursor = db.cursor()

  offset = (page - 1) * 50
  sql = "SELECT * FROM student OFFSET %s LIMIT 50"
  mycursor.execute(sql, (offset,))
  result = mycursor.fetchall()

  return result

def getAllStudents(search='', start=0, length=10):
    db = get_db()
    mycursor = db.cursor()
    
    if search:
      if search.isdigit() and len(search) == 1:
        mycursor.execute("SELECT * FROM student WHERE CAST(year_level AS TEXT) ILIKE %s ORDER BY student_id OFFSET %s LIMIT %s", (F'%{search}%', start, length))
      else:
        mycursor.execute("""
                        SELECT * FROM student 
                        WHERE student_id ILIKE %s OR 
                        first_name ILIKE %s OR 
                        last_name ILIKE %s OR 
                        CAST(year_level AS TEXT) ILIKE %s OR 
                        gender ILIKE %s OR 
                        program_code ILIKE %s 
                        ORDER BY student_id OFFSET %s LIMIT %s
                        """, (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%', start, length))
    else:
      mycursor.execute("""
                       SELECT * FROM student 
                       ORDER BY student_id
                       OFFSET %s LIMIT %s
                       """, (start, length))

    result = mycursor.fetchall()
    mycursor.close()
    return result

def getStudentCount(search=''):
  db = get_db()
  mycursor = db.cursor()

  if search:
    if search.isdigit() and len(search) == 1:
      mycursor.execute("SELECT COUNT (*) FROM student WHERE CAST(year_level AS TEXT) ILIKE %s", (f'%{search}%',))
    else:
      mycursor.execute("""
                      SELECT COUNT(*) FROM student
                      WHERE student_id ILIKE %s OR first_name ILIKE %s OR
                      last_name ILIKE %s OR
                      gender ILIKE %s OR program_code ILIKE %s
                      """, (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%'))
  else:
    mycursor.execute("SELECT COUNT(*) FROM student")

  result = mycursor.fetchone()[0]
  mycursor.close()

  return result