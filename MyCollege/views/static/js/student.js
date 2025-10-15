

$(document).ready(function () {
  const table = $('#studentTable').DataTable({
    processing: true,
    serverSide: true,
    ajax: {
      url: '/student/data',
      dataSrc: 'data',
      type: 'POST'
    },
    columns: [
      { data: 'id' },
      { data: 'fname' },
      { data: 'lname' },
      { data: 'year' },
      { data: 'gender' },
      { data: 'course' },
      {
        data: null,
        render: function (data, type, row) {
          return `
            <button class="btn btn-sm btn-warning edit-btn"
              data-id="${row.id}"
              data-fname="${row.fname}"
              data-lname="${row.lname}"
              data-year="${row.year}"
              data-gender="${row.gender}"
              data-course="${row.course}">
              Edit
            </button>
            <button class="btn btn-sm btn-danger delete-btn"
              data-id="${row.id}">
              Delete
            </button>
          `;
        }
      }
    ]
  });

  // ADD
  $('#submitStudAdd').click(function (e) {
    e.preventDefault();
    $.ajax({
      url: '/add_student',
      method: 'POST',
      data: {
        idAdd: $('#studentId').val(),
        firstNameAdd: $('#firstName').val(),
        lastNameAdd: $('#lastName').val(),
        courseAdd: $('#course').val(),
        yearAdd: $('#year').val(),
        genderAdd: $('#gender').val()
      },
      success: function () {
        $('#addModal').modal('hide');
        $('#idAdd').val('');
        $('#firstNameAdd').val('');
        $('#lastNameAdd').val('');
        $('#courseAdd').val('');
        $('#yearAdd').val('');
        $('#genderAdd').val('');
        showAlert('✅ Student added successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        showAlert('❌ Error adding student: ' + xhr.responseText, 'danger');
      }
    });
  });

  // EDIT
  $(document).on('click', '.edit-btn', function () {
    $('#studInitial').val($(this).data('id'));
    $('#studentIdEdit').val($(this).data('id'));
    $('#firstNameEdit').val($(this).data('fname'));
    $('#lastNameEdit').val($(this).data('lname'));
    $('#courseEdit').val($(this).data('course'));
    $('#yearEdit').val($(this).data('year'));
    $('#genderEdit').val($(this).data('gender'));
    $('#editModal').modal('show');
  });

  $('#submitStudEdit').click(function (e) {
    e.preventDefault();
    $.ajax({
      url: '/edit_student',
      method: 'POST',
      data: {
        studInitial: $('#studInitial').val(),
        idEdit: $('#studentIdEdit').val(),
        fnameEdit: $('#firstNameEdit').val(),
        lnameEdit: $('#lastNameEdit').val(),
        courseEdit: $('#courseEdit').val(),
        yearEdit: $('#yearEdit').val(),
        genderEdit: $('#genderEdit').val()
      },
      success: function () {
        $('#editModal').modal('hide');
        showAlert('✏️ Student updated successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        showAlert('❌ Error updating student: ' + xhr.responseText, 'danger');
      }
    });
  });

  // DELETE
  $(document).on('click', '.delete-btn', function () {
    $('#studDelete').val($(this).data('id'));
    $('#deleteModal').modal('show');
  });

  $('#submitStudDelete').click(function (e) {
    e.preventDefault();
    $.ajax({
      url: '/delete_student',
      method: 'POST',
      data: { studDelete: $('#studDelete').val() },
      success: function () {
        $('#deleteModal').modal('hide');
        showAlert('🗑️ Student deleted successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        showAlert('❌ Error deleting student: ' + xhr.responseText, 'danger');
      }
    });
  });

    function showAlert(message, type = 'success') {
    const alert = $(`
      <div class="alert alert-${type} alert-dismissible fade show mt-3" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `);
    $('.container').prepend(alert);
    setTimeout(() => alert.alert('close'), 3000);
  }
});
