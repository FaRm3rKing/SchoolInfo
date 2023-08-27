$(document).ready(function() {
  // Get the button element by its ID
  const addStudentBtn = $('#add-student');
  const deleteStudentBtn = $('#delete-student');

  // Add a click event listener to the add button
  addStudentBtn.on('click', function() {
    const fname = $('#entry-fname').val();
    const lname = $('#entry-lname').val();
    const email = $('#entry-email').val();
    $.ajax({
      url: "add-student/",
      method: 'POST',
      data: {
        "csrfmiddlewaretoken": CSRF_TOKEN,
        "fname": fname,
        "lname": lname,
        "email": email,
      },
      success: function(response) {
        $("#add-student-modal").modal('hide');
        alert("Student was added successfully.");
      },
      error: function(response) {
        // console.log(response);
        $("#add-student-modal").modal('hide');
        alert("Adding of student did not succeed.");
      },
    });
  });

  // Add a click event listener to the delete button
  deleteStudentBtn.on('click', function() {
    const studentId = $('#entry-id').val();
    const confirmation = $('#entry-confirmation').val();
    if (confirmation === 'TEU') {
      $.ajax({
        url: "delete-student/",
        method: 'POST',
        data: {
          "csrfmiddlewaretoken": CSRF_TOKEN,
          "student_id": studentId,
        },
        success: function(response) {
          $("#delete-student-modal").modal('hide');
          sleep(1)
          alert("Student was deleted successfully.");
        },
        error: function(response) {
          // console.log(response);
          $("#delete-student-modal").modal('hide');
          sleep(1)
          alert("Deletion of student did not succeed.");
        },
        complete: function(response) {
        }
      });
    } else {
      alert("Confirmation text is incorrect. Please type 'TEU' to confirm deletion.");
    }
  });

  $('#add-student-modal').on('hidden.bs.modal', function () {
    $(this).find('form').trigger('reset');
  });

  $('#delete-student-modal').on('hidden.bs.modal', function () {
    $(this).find('form').trigger('reset');
  });
});
