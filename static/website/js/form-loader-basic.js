document.getElementById("myForm").addEventListener("submit", function (e) {
  // Show the spinner
  document.getElementById("loading-container").style.display = "block";

  // Disable the submit button to prevent multiple submissions
  const submitBtn = document.getElementById("submitBtn");
  submitBtn.style.display = "none";
});
