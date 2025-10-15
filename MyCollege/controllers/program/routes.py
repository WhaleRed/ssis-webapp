from flask import request, jsonify
from . import program_bp
from MyCollege.models.program import *

@program_bp.route('/program/data')
def get_programs_data():
    programs = getAllPrograms()
    data = [{"code": row[0], "name": row[1], "college": row[2]} for row in programs]
    return jsonify({"data": data})

@program_bp.route('/add_program', methods=['POST'])
def add_program():
    progCode = request.form['progCodeAdd']
    progName = request.form['progNameAdd']
    colCode = request.form['colCodeAdd']
    addProgram([progCode, progName, colCode])
    return jsonify({'status': 'success', 'message': 'Program added successfully'})

@program_bp.route('/edit_program', methods=['POST'])
def edit_program():
    progInitial = request.form['progInitial']
    progCode = request.form['codeEdit']
    progName = request.form['nameEdit']
    progColCode = request.form['colEdit']
    editProgram([progCode, progName, progColCode, progInitial])
    return jsonify({'status': 'success', 'message': 'Program edited successfully'})

@program_bp.route('/delete_program', methods=['POST'])
def delete_program():
    code = request.form['progCodeDelete']
    deleteProgram([code])
    return jsonify({'status': 'success', 'message': 'Program deleted successfully'})
