from flask import request, jsonify
from . import program_bp
from MyCollege.models.program import *

@program_bp.route('/program/data', methods=['POST'])
def get_programs_data():
    try:
        #DataTables Parameter for server side
        draw = int(request.form.get('draw', 1))
        start = int(request.form.get('start', 0))
        length = int(request.form.get('length', 10))
        search_value = request.form.get('search[value]', '')

        #DataTables parameter for server side sorting
        order_column_index = request.form.get('order[0][column]', '0')
        order_dir = request.form.get('order[0][dir]', 'asc')

        #Map columns from DataTable to DB
        columns = ['program_code', 'program_name', 'college_code']
        order_column = columns[int(order_column_index)]

        #Data retrieval
        retrieve = getAllPrograms(search=search_value, start=start, length=length, order_column=order_column, order_dir=order_dir)
        total_records = getProgramCount()
        filtered_records = getProgramCount(search=search_value)

        data = [{'code': p[0], 'name': p[1], 'college': p[2]} for p in retrieve]

        return jsonify ({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })
    
    except Exception as e:
        return jsonify({'data': [], 'error': str(e)})

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

@program_bp.route('/get_colleges', methods=['GET'])
def get_colleges():
    try:
        colleges = getAllColleges()
        data = [{'code': c[0]} for c in colleges]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
