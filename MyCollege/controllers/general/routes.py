from flask import render_template
from . import general_bp
from MyCollege.models.college import *
from MyCollege.models.program import *
from MyCollege.models.student import *
from flask_login import login_required

@general_bp.route('/', endpoint="colleges")
@general_bp.route('/colleges')
@login_required
def colleges():
  data = populateCollege(1)
  return render_template("college.html", data = data)

@general_bp.route('/programs', endpoint="programs")
@login_required
def programs():
  data = populateProgram(1)
  return render_template("program.html", data = data)

@general_bp.route('/students', endpoint="students")
@login_required
def students():
  data = populateStudent(1)
  return render_template("student.html", data = data)