

$(document).ready(function () {
  let pendingData = null;

  function loadCourseDropdown(selectedCourse = null) {
    $.ajax({
      url: '/get_courses',
      method: 'GET',
      success: function (courses) {
        const dropdowns = $('#course, #courseEdit');
        dropdowns.empty();
        dropdowns.append('<option value="">Select Course</option>');

        courses.forEach(code => {
          const isSelected = selectedCourse === code ? 'selected' : '';
          dropdowns.append(`<option value="${code}" ${isSelected}>${code}</option>`);
        });
      },
      error: function (xhr) {
        console.error('Error loading courses:', xhr.responseText);
      }
    });
  }

  loadCourseDropdown();

  const table = $('#studentTable').DataTable({
    processing: true,
    serverSide: true,
    ajax: {
      url: '/student/data',
      dataSrc: 'data',
      type: 'POST'
    },
    columns: [
      {
        data: 'photo',
        render: function (data, type, row) {
          const url = data;
          return `<img src="${url}" 
                      class="img-thumbnail" 
                      style="width: 50px; height: 50px; object-fit: cover;">`;
        }
      },
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
              data-course="${row.course}"
              data-photo="${row.photo}">
              Edit
            </button>
            <button class="btn btn-sm btn-danger delete-btn"
              data-id="${row.id}">
              Delete
            </button>
          `;
        }
      }
    ],
    columnDefs: [
      {
        targets: [0, 7],
        orderable: false,
        searchable: false
      }
    ]
  });


  $('#addModal').on('show.bs.modal', function () {
    loadCourseDropdown();
  });

  // ADD
  $('#submitStudAdd').click(function (e) {
      e.preventDefault();

      const form = $('#addStudentForm')[0];
      const formData = new FormData(form);

      $.ajax({
          url: '/add_student',
          method: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function () {
              $('#addModal').modal('hide');
              form.reset();
              showAlert('✅ Student added successfully!');
              table.ajax.reload(null, false);
          },
          error: function (xhr) {
              let msg = 'An unknown error occurred.';
              try {
                  const response = JSON.parse(xhr.responseText);
                  msg = response.message || msg;
              } catch (e) {}
              showAlert('❌ ' + msg, 'danger');
          }
      });
  });


  // EDIT
  $(document).on('click', '.edit-btn', function () {
    $('#studInitial').val($(this).data('id'));
    $('#studentIdEdit').val($(this).data('id'));
    $('#firstNameEdit').val($(this).data('fname'));
    $('#lastNameEdit').val($(this).data('lname'));
    $('#yearEdit').val($(this).data('year'));
    $('#genderEdit').val($(this).data('gender'));
    $('#oldPhotoUrl').val($(this).data('photo'));
    $('#editModal').modal('show');

    loadCourseDropdown($(this).data('course'));
  });

  $('#submitStudEdit').click(function (e) {
    e.preventDefault();
    pendingData = {
      studInitial: $('#studInitial').val(),
      idEdit: $('#studentIdEdit').val(),
      fnameEdit: $('#firstNameEdit').val(),
      lnameEdit: $('#lastNameEdit').val(),
      courseEdit: $('#courseEdit').val(),
      yearEdit: $('#yearEdit').val(),
      genderEdit: $('#genderEdit').val()
    }

    $('#confirmEditModal').modal('show');
  });

  $('#confirmEditSave').on('click', function () {
      const formData = new FormData();
      formData.append('studInitial', $('#studInitial').val());
      formData.append('idEdit', $('#studentIdEdit').val());
      formData.append('fnameEdit', $('#firstNameEdit').val());
      formData.append('lnameEdit', $('#lastNameEdit').val());
      formData.append('courseEdit', $('#courseEdit').val());
      formData.append('yearEdit', $('#yearEdit').val());
      formData.append('genderEdit', $('#genderEdit').val());
      formData.append('oldPhotoUrl', $('#oldPhotoUrl').val());

      const file = $('#photoEdit')[0].files[0];
      if (file) {
          formData.append('photoEdit', file);
      }

      $.ajax({
          url: '/edit_student',
          method: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function () {
              $('#confirmEditModal').modal('hide');
              $('#editModal').modal('hide');
              showAlert('✏️ Student updated successfully!');
              table.ajax.reload(null, false);
          },
          error: function (xhr) {
              let msg = 'Error updating student.';
              try {
                  msg = JSON.parse(xhr.responseText).message;
              } catch {}
              showAlert('❌ ' + msg, 'danger');
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
