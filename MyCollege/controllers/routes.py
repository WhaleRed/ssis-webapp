from flask import render_template
from . import general_bp


@general_bp.route('/', endpoint="colleges")
@general_bp.route('/colleges')
def colleges():
  return render_template("college.html")

@general_bp.route('/programs', endpoint="programs")
def programs():
  return render_template("program.html")

@general_bp.route('/students', endpoint="students")
def students():
  return render_template("student.html")