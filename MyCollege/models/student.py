from MyCollege.supabase import get_db
import re

# functions take list as param

def addStudent(student):
    db = get_db()
    db.table("student").insert({
        "student_id": student[0],
        "first_name": student[1],
        "last_name": student[2],
        "year_level": student[3],
        "gender": student[4],
        "program_code": student[5]
    }).execute()


def deleteStudent(idnum):
    db = get_db()
    db.table("student").delete().eq("student_id", idnum).execute()


def editStudent(student):
    db = get_db()
    db.table("student").update({
        "student_id": student[0],
        "first_name": student[1],
        "last_name": student[2],
        "year_level": student[3],
        "gender": student[4],
        "program_code": student[5]
    }).eq("student_id", student[6]).execute()


def populateStudent(page):
    db = get_db()
    offset = (page - 1) * 50
    response = db.table("student").select("*").offset(offset).limit(50).execute()
    return response.data  # list of dicts


def getAllStudents(search='', start=0, length=10, order_column='student_id', order_dir='asc'):
    db = get_db()
    order_desc = True if order_dir.lower() == "desc" else False

    query = db.table("student").select("*")

    if search:
        if search.isdigit() and len(search) == 1:
            query = query.filter("year_level", "ilike", f"%{search}%")
        else:
            query = query.or_(
                f"student_id.ilike.*{search}*,first_name.ilike.*{search}*,last_name.ilike.*{search}*,gender.ilike.*{search}*,program_code.ilike.*{search}*"
            )

    response = query.order(order_column, desc=order_desc).offset(start).limit(length).execute()
    return response.data  # list of dicts


def getStudentCount(search=''):
    db = get_db()
    query = db.table("student").select("student_id", count="exact")

    if search:
        if search.isdigit() and len(search) == 1:
            query = query.filter("year_level", "ilike", f"%{search}%")
        else:
            query = query.or_(
                f"student_id.ilike.*{search}*,first_name.ilike.*{search}*,last_name.ilike.*{search}*,gender.ilike.*{search}*,program_code.ilike.*{search}*"
            )

    response = query.execute()
    return response.count or 0



def getCourses():
    db = get_db()
    response = db.table("program").select("program_code").execute()
    return [row["program_code"] for row in response.data]


def validateId(studentId):
    pattern = r'^\d{4}-\d{4}$'
    return bool(re.match(pattern, studentId))
