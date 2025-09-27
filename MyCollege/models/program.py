from ...db import get_db

def addProgram(program):
  db = get_db()
  mycursor = db.cursor()

  sql = "INSERT INTO program(program_code, program_name, college_code) VALUES (%s, %s, %s)"
  mycursor.execute(sql, program)
  db.commit()

  mycursor.close()