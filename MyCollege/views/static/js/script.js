//For CSRF
$(function () {
  $.ajaxSetup({
    headers: {
      'X-CSRFToken': $('input[name="csrf_token"]').val()
    }
  });
});
