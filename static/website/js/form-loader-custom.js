document.getElementById("myForm").addEventListener("submit", function (e) {
  // Show the spinner
  document.getElementById("loading-container").style.display = "block";

  // Disable the submit button to prevent multiple submissions
  const submitBtn = document.getElementById("submitBtn");
  submitBtn.style.display = "none";

  const myTitle = document.getElementById("myTitle");
  myTitle.style.display = "none";

  // Set a minimum display time for the spinner (3 seconds)
  setTimeout(function () {
    // Now you can submit the form programmatically after the minimum display time
    // Replace 'myForm' with your form id if it's different
    document.getElementById("myForm").submit();
  }, 2000); // 2000 milliseconds = 2 seconds

  // Prevent the default form submission behavior
  e.preventDefault();
});
