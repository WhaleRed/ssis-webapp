from flask import request, redirect, url_for, flash, jsonify
from . import student_bp
from MyCollege.models.student import *
import psycopg2
from psycopg2 import errors
from flask_login import login_required
from ...supabase import supabase
import uuid

@student_bp.route('/student/data', methods=['POST'])
@login_required
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
            'course': s[5],
            'photo': s[6]
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
@login_required
def add_student():
    try:
        studId = request.form.get('idAdd')
        fname = request.form.get('firstNameAdd')
        lname = request.form.get('lastNameAdd')
        course = request.form.get('courseAdd')
        year = request.form.get('yearAdd')
        gender = request.form.get('genderAdd')
        photo = request.files.get('photoAdd')

        if not all([studId, fname, lname, course, year, gender]):
            return jsonify({'success': False, 'message': 'All fields are required!'}), 400

        # Default photo URL
        photo_url = "https://vgygdysxpdxoodvwmvwj.supabase.co/storage/v1/object/public/student-img/default.jpg"

        # Upload photo if provided
        if photo:
            unique_filename = f"{uuid.uuid4()}_{photo.filename}"
            file_path = f"{studId}/{unique_filename}"

            res = supabase.storage.from_("student-img").upload(
                file_path,
                photo.read(),
                file_options={"content-type": photo.mimetype}
            )

            photo_url = supabase.storage.from_("student-img").get_public_url(file_path)

        student = [studId, fname, lname, year, gender, course, photo_url]
        addStudent(student)

        return jsonify({"message": "Student added successfully"})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@student_bp.route('/edit_student', methods=['POST'])
@login_required
def edit_student():
    try:
        studInitial = request.form['studInitial']
        studId = request.form['idEdit']
        fname = request.form['fnameEdit']
        lname = request.form['lnameEdit']
        course = request.form['courseEdit']
        year = request.form['yearEdit']
        gender = request.form['genderEdit']
        old_photo = request.form.get('oldPhotoUrl')

        photo = request.files.get('photoEdit')

        if not all([studId, fname, lname, course, year, gender]):
            return jsonify({'success': False, 'message': 'All fields are required!'}), 400

        if not validateId(studId):
            return jsonify({
                'success': False,
                'message': 'Invalid Student ID format. Use YYYY-NNNN.'
            }), 400

        photo_url = old_photo
        if photo:
            unique_filename = f"{uuid.uuid4()}_{photo.filename}"
            file_path = f"{studId}/{unique_filename}"

            res = supabase.storage.from_("student-img").upload(
                file_path,
                photo.read(),
                file_options={"content-type": photo.mimetype}
            )


            photo_url = supabase.storage.from_("student-img").get_public_url(file_path)

            if old_photo and "default.jpg" not in old_photo:
                old_path = old_photo.split("/student-img/")[1]
                supabase.storage.from_("student-img").remove([old_path])

        # Update DB
        student = [studId, fname, lname, year, gender, course, photo_url, studInitial]
        editStudent(student)

        return jsonify({"message": "Student updated successfully"})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500



@student_bp.route('/delete_student', methods=['POST'])
@login_required
def delete_student():
    try:
        studid = request.form['studDelete']
        student = [studid]
        deleteStudent(student)
        return jsonify({"message": "Student deleted successfully"})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@student_bp.route('/get_courses')
@login_required
def get_all_courses():
    try:
        courses = getCourses()
        # Return plain list of course codes
        return jsonify([c[0] for c in courses])
    except Exception as e:
        return jsonify({'error': str(e)}), 500