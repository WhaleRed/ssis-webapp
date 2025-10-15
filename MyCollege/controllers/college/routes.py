from flask import request, jsonify
from . import college_bp
from MyCollege.models.college import *

@college_bp.route('/college/data', methods=['POST'])
def get_colleges_data():
    try:
        #DataTables Parameter for server side
        draw = int(request.form.get('draw', 1))
        start = int(request.form.get('start', 0))
        length = int(request.form.get('length', 10))
        search_value = request.form.get('search[value]', '')

        #Data retrieval
        retrieve = getAllColleges(search=search_value, start=start, length=length)
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
def add_college():
    try:
        colCode = request.form['colCodeAdd']
        colName = request.form['colNameAdd']

        addCollege([colCode, colName])
        return jsonify({'success': True, 'message': 'College added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})



@college_bp.route('/edit_college', methods=['POST'])
def edit_college():
    try:
        colInitial = request.form['colInitial']
        colCode = request.form['codeEdit']
        colName = request.form['nameEdit']

        editCollege([colCode, colName, colInitial])
        return jsonify({'success': True, 'message': 'College updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@college_bp.route('/delete_college', methods=['POST'])
def delete_college():
    try:
        code = request.form['colCodeDelete']
        deleteCollege([code])
        return jsonify({'success': True, 'message': 'College deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    