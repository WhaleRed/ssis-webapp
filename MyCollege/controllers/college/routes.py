from flask import request, jsonify
from flask_login import login_required
from . import college_bp
from MyCollege.models.college import *
import psycopg2
from psycopg2 import errors

@college_bp.route('/college/data', methods=['POST'])
@login_required
def get_colleges_data():
    try:
        #DataTables Parameter for server side pagination and search
        draw = int(request.form.get('draw', 1))
        start = int(request.form.get('start', 0))
        length = int(request.form.get('length', 10))
        search_value = request.form.get('search[value]', '')

        #DataTables Parameter for server side sorting
        order_column_index = request.form.get('order[0][column]', '0')
        order_dir = request.form.get('order[0][dir]', 'asc')

        #Map columns from DataTables to DB
        columns = ['college_code', 'college_name']
        order_column = columns[int(order_column_index)]


        #Data retrieval
        retrieve = getAllColleges(search=search_value, start=start, length=length, order_column=order_column, order_dir=order_dir)
        total_records = getCollegeCount()
        filtered_records = getCollegeCount(search=search_value)

        data = [{'code': c[0], 'name': c[1]} for c in retrieve]

        return jsonify ({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })

    except Exception as e:
        return jsonify({'data': [], 'error': str(e)})


@college_bp.route('/add_college', methods=['POST'])
@login_required
def add_college():
    try:
        colCode = request.form['colCodeAdd'].strip()
        colName = request.form['colNameAdd'].strip()

        if not colCode or not colName:
            return jsonify({'success': False, 'message': 'All fields are required!'}), 400
        
        addCollege([colCode, colName])
        return jsonify({'success': True, 'message': 'College added successfully'})
    #Exceptions
    except psycopg2.errors.UniqueViolation:
        return jsonify({'success': False, 'message': 'College code or name already exists!'}), 400
    except psycopg2.errors.NotNullViolation:
        return jsonify({'success': False, 'message': 'All fields are required!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})



@college_bp.route('/edit_college', methods=['POST'])
@login_required
def edit_college():
    try:
        colInitial = request.form['colInitial']
        colCode = request.form.get('codeEdit', '').strip()
        colName = request.form.get('nameEdit', '').strip()

        if not colCode or not colName:
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        editCollege([colCode, colName, colInitial])
        return jsonify({'success': True, 'message': 'College updated successfully'})
    #Exceptions
    except psycopg2.errors.UniqueViolation:
        return jsonify({'success': False, 'message': 'College code or name already exists!'}), 400
    except psycopg2.errors.NotNullViolation:
        return jsonify({'success': False, 'message': 'All fields are required!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@college_bp.route('/delete_college', methods=['POST'])
@login_required
def delete_college():
    try:
        code = request.form['colCodeDelete']
        deleteCollege([code])
        return jsonify({'success': True, 'message': 'College deleted successfully'})
    #Exceptions
    except psycopg2.errors.ForeignKeyViolation:
        return jsonify({'success': False, 'message': 'Cannot delete this college because it is referenced by one or more programs.'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    