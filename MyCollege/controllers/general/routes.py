from flask import render_template
from . import general_bp
from MyCollege.models.college import *
from MyCollege.models.program import *
from MyCollege.models.student import *

@general_bp.route('/', endpoint="colleges")
@general_bp.route('/colleges')
def colleges():
  data = populateCollege(1)
  return render_template("college.html", data = data)

@general_bp.route('/programs', endpoint="programs")
def programs():
  data = populateProgram(1)
  return render_template("program.html", data = data)

@general_bp.route('/students', endpoint="students")
def students():
  data = populateStudent(1)
  return render_template("student.html", data = data)