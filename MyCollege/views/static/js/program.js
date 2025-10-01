const editModal = document.getElementById('editModal');

if (editModal) {
  editModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    // Get data from button
    const code = button.getAttribute('edit-code');
    const name = button.getAttribute('edit-name');
    const college = button.getAttribute('edit-college')

    // Fill form fields
    document.getElementById('progCodeInitial').value = code;
    document.getElementById('progCodeEdit').value = code;
    document.getElementById('progNameEdit').value = name;
    document.getElementById('progColCodeEdit').value = college
  });
}