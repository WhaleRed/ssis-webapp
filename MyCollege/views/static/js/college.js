const editModal = document.getElementById('editModal');
const deleteModal = document.getElementById('deleteModal');

if (editModal) {
  editModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    // Get data from button
    const code = button.getAttribute('edit-code');
    const name = button.getAttribute('edit-name');

    // Fill form fields
    document.getElementById('colCodeInitial').value = code;
    document.getElementById('colCodeEdit').value = code;
    document.getElementById('colNameEdit').value = name;
  });
}

if (deleteModal) {
  deleteModal.addEventListener('show.bs.modal', function (event){
    const button = event.relatedTarget;

    //Get data from button
    const code = button.getAttribute('del-code');

    //Fill hidden input
    document.getElementById('colCodeDelete').value = code;
  });
}