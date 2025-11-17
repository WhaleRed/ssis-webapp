from MyCollege.supabase import get_db


def addCollege(college):
    db = get_db()
    db.table("college").insert({
        "college_code": college[0],
        "college_name": college[1]
    }).execute()


def deleteCollege(college_code):
    db = get_db()
    db.table("college").delete().eq("college_code", college_code).execute()


def editCollege(college):
    db = get_db()
    db.table("college").update({
        "college_code": college[0],
        "college_name": college[1]
    }).eq("college_code", college[2]).execute()


def populateCollege(page):
    db = get_db()
    offset = (page - 1) * 10
    response = db.table("college").select("*").offset(offset).limit(10).execute()
    return response.data  # list of dictionaries


def getAllColleges(search='', start=0, length=10, order_column='college_code', order_dir='asc'):
    db = get_db()
    order_desc = True if order_dir.lower() == "desc" else False

    query = db.table("college").select("*")

    if search:
        query = query.or_(
            f"college_code.ilike.%{search}%,college_name.ilike.%{search}%"
        )

    response = query.order(order_column, desc=order_desc).offset(start).limit(length).execute()

    return [{"code": c["college_code"], "name": c["college_name"]} for c in response.data]


def getCollegeCount(search=''):
    db = get_db()
    query = db.table("college").select("college_code", count="exact")

    if search:
        query = query.or_(
            f"college_code.ilike.%{search}%,college_name.ilike.%{search}%"
        )

    response = query.execute()
    return response.count or 0
