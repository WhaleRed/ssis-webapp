from flask import request, redirect, url_for, flash, jsonify
from . import student_bp
from MyCollege.models.student import *

@student_bp.route('/student/data', methods=['POST'])
def get_students_data():
    try:
        #DataTables Param for server side
        draw = int(request.form.get('draw', 1))
        start = int(request.form.get('start', 0))
        length = int(request.form.get('length', 10))
        search_value = request.form.get('search[value]', '')

        #DataTables parameter for serverside sorting
        order_column_index = request.form.get('order[0][column]', '0')
        order_dir = request.form.get('order[0][dir]', 'asc')

        #Map columns from DataTables to DB
        columns = ['student_id', 'first_name', 'last_name', 'year_level', 'gender', 'program_code']
        order_column = columns[int(order_column_index)]

        retrieve = getAllStudents(search=search_value, start=start, length=length, order_column=order_column, order_dir=order_dir)
        total_records = getStudentCount()
        filtered_records = getStudentCount(search=search_value)

        data = [{
            'id': s[0],
            'fname': s[1],
            'lname': s[2],
            'year': s[3],
            'gender': s[4],
            'course': s[5]
        } for s in retrieve]

        return jsonify ({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })
    except Exception as e:
        return jsonify({'data': [], 'error': str(e)})


@student_bp.route('/add_student', methods=['POST'])
def add_student():
    studId = request.form['idAdd']
    fname = request.form['firstNameAdd']
    lname = request.form['lastNameAdd']
    course = request.form['courseAdd']
    year = request.form['yearAdd']
    gender = request.form['genderAdd']

    student = [studId, fname, lname, year, gender, course]
    addStudent(student)
    return jsonify({"message": "Student added successfully"})


@student_bp.route('/edit_student', methods=['POST'])
def edit_student():
    studInitial = request.form['studInitial']
    studId = request.form['idEdit']
    fname = request.form['fnameEdit']
    lname = request.form['lnameEdit']
    course = request.form['courseEdit']
    year = request.form['yearEdit']
    gender = request.form['genderEdit']

    student = [studId, fname, lname, year, gender, course, studInitial]
    editStudent(student)
    return jsonify({"message": "Student updated successfully"})


@student_bp.route('/delete_student', methods=['POST'])
def delete_student():
    studid = request.form['studDelete']
    student = [studid]
    deleteStudent(student)
    return jsonify({"message": "Student deleted successfully"})
