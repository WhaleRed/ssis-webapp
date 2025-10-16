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

def populateProgram(page):
  db = get_db()
  mycursor = db.cursor()

  offset = (page - 1) * 25
  sql = "SELECT * FROM program OFFSET %s LIMIT 25"
  mycursor.execute(sql, (offset,))
  result = mycursor.fetchall()

  return result

def getAllPrograms(search='', start=0, length=10, order_column='program_code', order_dir='asc'):
  db = get_db()
  mycursor = db.cursor()
  order_dir = 'ASC' if order_dir.lower() == 'asc' else 'DESC'

  query = "SELECT * FROM program"
  params = []

  if search:
    query += " WHERE program_code ILIKE %s OR program_name ILIKE %s OR college_code ILIKE %s"
    params = [f'%{search}%', f'%{search}%', f'%{search}%']
  
  query += f" ORDER BY {order_column} {order_dir} OFFSET %s LIMIT %s"
  params.extend([start, length])

  mycursor.execute(query, params)

  result = mycursor.fetchall()
  mycursor.close()
  return result

def getProgramCount(search=''):
  db = get_db()
  mycursor = db.cursor()

  if search:
    mycursor.execute("""
                     SELECT COUNT(*) FROM program
                     WHERE program_code ILIKE %s OR program_name ILIKE %s OR college_code ILIKE %s
                     """, (f'%{search}%', f'%{search}%', f'%{search}%'))
  else:
    mycursor.execute("SELECT COUNT(*) FROM program")

  count = mycursor.fetchone()[0]
  mycursor.close()

  return count