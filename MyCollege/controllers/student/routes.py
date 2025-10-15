from flask import request, redirect, url_for, flash, jsonify
from . import student_bp
from MyCollege.models.student import *

@student_bp.route('/student/data')
def get_students_data():
    data = getAllStudents()
    
    students = [
        {
            'id': row[0],
            'fname': row[1],
            'lname': row[2],
            'year': row[3],
            'gender': row[4],
            'course': row[5]
        }
        for row in data
    ]
    return jsonify({"data": students})


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
