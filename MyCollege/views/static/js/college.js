const editModal = document.getElementById('editModal');
const deleteModal = document.getElementById('deleteModal');
let pendingData = null;

if (editModal) {
  editModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const code = button.getAttribute('edit-code');
    const name = button.getAttribute('edit-name');

    document.getElementById('colCodeInitial').value = code;
    document.getElementById('colCodeEdit').value = code;
    document.getElementById('colNameEdit').value = name;
  });
}

if (deleteModal) {
  deleteModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const code = button.getAttribute('del-code');
    document.getElementById('colCodeDelete').value = code;
  });
}


$(document).ready(function () {

  const table = $('#colTable').DataTable({
    processing: true,
    serverSide: true,
    ajax: {
      url: '/college/data',
      dataSrc: 'data',
      type: 'POST'
    },
    columns: [
      { data: 'code' },
      { data: 'name' },
      {
        data: null,
        render: function (row) {
          return `
            <button class="btn btn-sm btn-warning" data-bs-toggle="modal"
              data-bs-target="#editModal" edit-code="${row.code}" edit-name="${row.name}">
              Edit
            </button>
            <button class="btn btn-sm btn-danger" data-bs-toggle="modal"
              data-bs-target="#deleteModal" del-code="${row.code}">
              Delete
            </button>
          `;
        }
      }
    ],
    columnDefs: [
      {
        targets: [2],
        orderable: false,
        searchable: false
      }
    ]
  });

  $('#submitColAdd').on('click', function (e) {
    e.preventDefault();
    const colCode = $('#colCode').val();
    const colName = $('#colName').val();

    $.ajax({
      url: '/add_college',
      type: 'POST',
      data: { colCodeAdd: colCode, colNameAdd: colName },
      success: function () {
        $('#addModal').modal('hide');
        $('#colCode').val('');
        $('#colName').val('');
        showAlert('✅ College added successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        handleAjaxError(xhr, 'Error adding college.');
      }
    });
  });

  $('#submitColEdit').on('click', function (e) {
    e.preventDefault();

    pendingData = {
      colInitial: $('#colCodeInitial').val(),
      codeEdit: $('#colCodeEdit').val(),
      nameEdit: $('#colNameEdit').val()
    };

    $('#confirmEditModal').modal('show');
  });

  $('#confirmEditSave').on('click', function () {
    if (!pendingData) return;

    $.ajax({
      url: '/edit_college',
      type: 'POST',
      data: pendingData,
      success: function () {
        $('#confirmEditModal').modal('hide');
        $('#editModal').modal('hide');
        showAlert('✏️ College updated successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        handleAjaxError(xhr, 'Error updating college.');
      }
    });
  });

  $('#submitColDelete').on('click', function (e) {
    e.preventDefault();
    const colCode = $('#colCodeDelete').val();

    $.ajax({
      url: '/delete_college',
      type: 'POST',
      data: { colCodeDelete: colCode },
      success: function () {
        $('#deleteModal').modal('hide');
        showAlert('🗑️ College deleted successfully!');
        table.ajax.reload(null, false);
      },
      error: function (xhr) {
        showAlert('❌ Error deleting college: ' + xhr.responseText, 'danger');
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
