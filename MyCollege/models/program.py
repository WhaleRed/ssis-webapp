from MyCollege.db import get_db

#functions takes list as param

def addProgram(program):
  db = get_db()
  mycursor = db.cursor()

  sql = "INSERT INTO program(program_code, program_name, college_code) VALUES (%s, %s, %s)"
  mycursor.execute(sql, program)
  db.commit()

  mycursor.close()

def deleteProgram(program_code):    
  db = get_db()
  mycursor = db.cursor()

  mycursor.execute("DELETE FROM program WHERE program_code = %s", program_code)
  db.commit()
  
  mycursor.close()

def editProgram(program):
  db = get_db()
  mycursor = db.cursor()
  
  sql = "UPDATE program SET program_code = %s, program_name = %s, college_code = %s WHERE program_code =%s"
  mycursor.execute(sql, program)
  db.commit()

  mycursor.close()