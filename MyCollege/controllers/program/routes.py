from flask import request, redirect, url_for, flash
from . import program_bp
from MyCollege.models.program import *

@program_bp.route('/add_program', methods = ['POST'])
def add_program():
  if request.method == 'POST':
    progCode = request.form['progCodeAdd']
    progName = request.form['progNameAdd']
    colCode = request.form['colCodeAdd']

    program = [progCode, progName, colCode]
    addProgram(program)
    flash('Program Added Succesfully')

    return redirect(url_for('general.programs'))
  
@program_bp.route('/edit_program', methods = ['POST'])
def edit_program():
  if request.method == 'POST':
    progInitial = request.form['progInitial']
    progCode = request.form['codeEdit']
    progName = request.form['nameEdit']
    progColCode = request.form['colEdit']

    program = [progCode, progName, progColCode, progInitial]
    editProgram(program)
    flash('Program Edited Succesfully')
    
    return redirect(url_for('general.programs'))