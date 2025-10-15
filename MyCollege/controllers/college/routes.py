from flask import request, jsonify
from . import college_bp
from MyCollege.models.college import addCollege, editCollege, deleteCollege, getAllColleges

@college_bp.route('/college/data')
def get_colleges_data():
    try:
        colleges = getAllColleges() 
        data = [{'code': c[0], 'name': c[1]} for c in colleges]
        return jsonify({'data': data})
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
    
@college_bp.route('/data')
def get_college_data():
    colleges = getAllColleges()

    data = [{'code': c[0], 'name': c[1]} for c in colleges]

    return jsonify({'data': data})