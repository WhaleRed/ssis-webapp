from flask import request, redirect, url_for, flash
from . import student_bp
from MyCollege.models.student import *

@student_bp.route('/add_student', methods = ['POST'])
def add_student():
  if request.method == 'POST':
    studId = request.form['idAdd']
    fname = request.form['firstNameAdd']
    lname = request.form['lastNameAdd']
    course = request.form['courseAdd']
    year = request.form['yearAdd']
    gender = request.form['genderAdd']

    student = [studId, fname, lname, year, gender, course]
    addStudent(student)
    flash('Student Added Succesfully')

    return redirect(url_for('general.students'))
  
@student_bp.route('/edit_student', methods = ['POST'])
def edit_student():
  if request.method == 'POST':
    studInitial = request.form['studInitial']
    studId = request.form['idEdit']
    fname = request.form['fnameEdit']
    lname = request.form['lnameEdit']
    course = request.form['courseEdit']
    year = request.form['yearEdit']
    gender = request.form['genderEdit']

    student = [studId, fname, lname, year, gender, course, studInitial]
    editStudent(student)
    flash('Student Edited Succesfully')

    return redirect(url_for('general.students'))