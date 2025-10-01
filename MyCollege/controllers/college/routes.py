from flask import request, redirect, url_for, flash
from . import college_bp
from MyCollege.models.college import *

@college_bp.route('/add_college', methods = ['POST'])
def add_college():
  if request.method == 'POST':
    colCode = request.form['colCodeAdd']
    colName = request.form['colNameAdd']

    college = [colCode, colName]
    addCollege(college)
    flash('College Added Succesfully')

    return redirect(url_for('general.colleges'))
  
@college_bp.route('/edit_college', methods = ['POST'])
def edit_college():
  if request.method == 'POST':
    colInitial = request.form['colInitial']
    colCode = request.form['codeEdit']
    colName = request.form['nameEdit']

    college = [colCode, colName, colInitial]
    editCollege(college)
    flash('College Edited Succesfully')

    return redirect(url_for('general.colleges'))
  
@college_bp.route('/delete_college', methods = ['POST'])
def delete_college():
  if request.method == 'POST':
    code = request.form['colCodeDelete']

    college = [code]
    deleteCollege(college)
    flash('College Deleted Succesfully')
    return redirect(url_for('general.colleges'))