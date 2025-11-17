from MyCollege.supabase import get_db

# functions take list as param

def addProgram(program):
    db = get_db()
    db.table("program").insert({
        "program_code": program[0],
        "program_name": program[1],
        "college_code": program[2]
    }).execute()


def deleteProgram(program_code):
    db = get_db()
    db.table("program").delete().eq("program_code", program_code).execute()


def editProgram(program):
    db = get_db()
    db.table("program").update({
        "program_code": program[0],
        "program_name": program[1],
        "college_code": program[2]
    }).eq("program_code", program[3]).execute()


def populateProgram(page):
    db = get_db()
    offset = (page - 1) * 25
    response = db.table("program").select("*").offset(offset).limit(25).execute()
    return response.data  # list of dictionaries


def getAllPrograms(search='', start=0, length=10, order_column='program_code', order_dir='asc'):
    db = get_db()
    order_desc = True if order_dir.lower() == "desc" else False

    query = db.table("program").select("*")

    if search:
        query = query.or_(
            f"program_code.ilike.*{search}*,program_name.ilike.*{search}*,college_code.ilike.*{search}*"
        )

    response = query.order(order_column, desc=order_desc).offset(start).limit(length).execute()
    return response.data


def getProgramCount(search=''):
    db = get_db()
    query = db.table("program").select("program_code", count="exact")

    if search:
        query = query.or_(
            f"program_code.ilike.*{search}*,program_name.ilike.*{search}*,college_code.ilike.*{search}*"
        )

    response = query.execute()
    return response.count or 0


def getAllColleges():
    db = get_db()
    response = db.table("college").select("college_code").execute()
    # return list of codes instead of list of dicts
    return [row["college_code"] for row in response.data]
