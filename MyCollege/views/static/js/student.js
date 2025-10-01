const editModal = document.getElementById('editModal');
const deleteModal = document.getElementById('deleteModal');

if (editModal) {
  editModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    // Get data from button
    const studId = button.getAttribute('edit-id');
    const fname = button.getAttribute('edit-fname');
    const lname = button.getAttribute('edit-lname');
    const year = button.getAttribute('edit-year');
    const gender = button.getAttribute('edit-gender');
    const course = button.getAttribute('edit-course');

    // Fill form fields
    document.getElementById('studInitial').value = studId
    document.getElementById('studentIdEdit').value = studId
    document.getElementById('firstNameEdit').value = fname
    document.getElementById('lastNameEdit').value = lname
    document.getElementById('courseEdit').value = course
    document.getElementById('yearEdit').value = year
    document.getElementById('genderEdit').value = gender
  });
}

if (deleteModal) {
  deleteModal.addEventListener('show.bs.modal', function (event){
    const button = event.relatedTarget;

    //Get data from button
    const studid = button.getAttribute('del-stud');

    //Fill hidden input
    document.getElementById('studDelete').value = studid;
  });
}