

$(document).ready(function () {
  let pendingData = null;

  function loadCollegeDropdown(selectedCode = null) {
    $.ajax({
      url: '/get_colleges',
      method: 'GET',
      success: function (data) {
        const colCodeSelect = $('#colCode');
        const colCodeEditSelect = $('#progColCodeEdit');

        colCodeSelect.empty().append('<option value="">Select College</option>');
        colCodeEditSelect.empty().append('<option value="">Select College</option>');

        data.forEach(col => {
          const option = `<option value="${col.code}">${col.code}</option>`;
          colCodeSelect.append(option);
          colCodeEditSelect.append(option);
        });

        if (selectedCode) {
          colCodeEditSelect.val(selectedCode);
        }
      },
      error: function (xhr) {
        console.error('Error loading colleges:', xhr.responseText);
      }
    });
  }

  loadCollegeDropdown();

  $('#addModal').on('show.bs.modal', function () {
    loadCollegeDropdown();
  });

  $('#editModal').on('show.bs.modal', function () {
    loadCollegeDropdown();
  });

  const table = $('#programTable').DataTable({
    processing: true,
    serverSide: true,
    ajax: {
      url: '/program/data',
      dataSrc: 'data',
      type: 'POST'
    },
    columns: [
      { data: 'code' },
      { data: 'name' },
      { data: 'college' },
      {
        data: null,
        render: function (data, type, row) {
          return `
            <button class="btn btn-sm btn-warning edit-btn" data-code="${row.code}" data-name="${row.name}" data-college="${row.college}">Edit</button>
            <button class="btn btn-sm btn-danger delete-btn" data-code="${row.code}">Delete</button>
          `;
        }
      }
    ],
    columnDefs: [
      {
        targets: [3],
        orderable: false,
        searchable: false
      }
    ]
  });


  $('#submitProgAdd').click(function (e) {
    e.preventDefault();
    $.ajax({
      url: '/add_program',
      method: 'POST',
      data: {
        progCodeAdd: $('#progCode').val(),
        progNameAdd: $('#progName').val(),
        colCodeAdd: $('#colCode').val()
      },
      success: function () {
        $('#addModal').modal('hide');
        $('#progCodeAdd').val('');
        $('#progNameAdd').val('');
        $('#colCodeAdd').val('');
        showAlert('✅ Program added successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        handleAjaxError(xhr, 'Error adding program.');
      }
    });
  });


  $(document).on('click', '.edit-btn', function () {
    $('#progCodeInitial').val($(this).data('code'));
    $('#progCodeEdit').val($(this).data('code'));
    $('#progNameEdit').val($(this).data('name'));
    $('#progColCodeEdit').val($(this).data('college'));
    $('#editModal').modal('show');

    loadCollegeDropdown($(this).data('college'));
  });


  $('#submitProgEdit').click(function (e) {
    e.preventDefault();

    pendingData = {
      progInitial: $('#progCodeInitial').val(),
      codeEdit: $('#progCodeEdit').val(),
      nameEdit: $('#progNameEdit').val(),
      colEdit: $('#progColCodeEdit').val()
    }

    $('#confirmEditModal').modal('show');
  });

  $('#confirmEditSave').on('click', function () {
    if (!pendingData) return;

    $.ajax({
      url: '/edit_program',
      method: 'POST',
      data: pendingData,
      success: function () {
        $('#confirmEditModal').modal('hide');
        $('#editModal').modal('hide');
        showAlert('✏️ Program updated successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        handleAjaxError(xhr, 'Error updating program.');
      }
    });
  });

  $(document).on('click', '.delete-btn', function () {
    $('#progCodeDelete').val($(this).data('code'));
    $('#deleteModal').modal('show');
  });


  $('#submitProgDelete').click(function (e) {
    e.preventDefault();
    $.ajax({
      url: '/delete_program',
      method: 'POST',
      data: { progCodeDelete: $('#progCodeDelete').val() },
      success: function () {
        $('#deleteModal').modal('hide');
        showAlert('🗑️ Program deleted successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        showAlert('❌ Error deleting program: ' + xhr.responseText, 'danger');
      }
    });
  });

  function handleAjaxError(xhr, defaultMsg) {
    let msg = defaultMsg;
    try {
      const response = JSON.parse(xhr.responseText);
      msg = response.message || msg;
    } catch (e) {
      msg = xhr.responseText;
    }
    showAlert('❌ ' + msg, 'danger');
  }

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
