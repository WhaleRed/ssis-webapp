from flask import request, jsonify
from . import program_bp
from MyCollege.models.program import *
import psycopg2
from psycopg2 import errors
from flask_login import login_required

@program_bp.route('/program/data', methods=['POST'])
@login_required
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
@login_required
def add_program():
    try:
        progCode = request.form['progCodeAdd']
        progName = request.form['progNameAdd']
        colCode = request.form['colCodeAdd']

        if not progCode or not progName or not colCode:
            return jsonify({'success': False, 'message': 'All fields are required!'}), 400
        
        addProgram([progCode, progName, colCode])
        return jsonify({'status': 'success', 'message': 'Program added successfully'})
    
    #Exceptions
    except psycopg2.errors.UniqueViolation:
        return jsonify({'success': False, 'message': 'Program code or name already exists!'}), 400
    except psycopg2.errors.NotNullViolation:
        return jsonify({'success': False, 'message': 'All fields are required!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@program_bp.route('/edit_program', methods=['POST'])
@login_required
def edit_program():
    try:
        progInitial = request.form['progInitial']
        progCode = request.form['codeEdit']
        progName = request.form['nameEdit']
        progColCode = request.form['colEdit']

        if not progCode or not progName or not progColCode:
            return jsonify({'success': False, 'message': 'All fields are required!'}), 400
        
        editProgram([progCode, progName, progColCode, progInitial])
        return jsonify({'status': 'success', 'message': 'Program edited successfully'})
    #Exceptions
    except psycopg2.errors.UniqueViolation:
        return jsonify({'success': False, 'message': 'Program code or name already exists!'}), 400
    except psycopg2.errors.NotNullViolation:
        return jsonify({'success': False, 'message': 'All fields are required!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@program_bp.route('/delete_program', methods=['POST'])
@login_required
def delete_program():
    try:
        code = request.form['progCodeDelete']
        deleteProgram([code])
        return jsonify({'status': 'success', 'message': 'Program deleted successfully'})
    #Exceptions
    except psycopg2.errors.ForeignKeyViolation:
        return jsonify({'success': False, 'message': 'Cannot delete this program because it is referenced by one or more students.'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@program_bp.route('/get_colleges', methods=['GET'])
@login_required
def get_colleges():
    try:
        colleges = getAllColleges()
        data = [{'code': c[0]} for c in colleges]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
