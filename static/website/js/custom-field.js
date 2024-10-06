$(document).ready(function () {
  $("#switchCheckDefault").change(function () {
    if (this.checked) {
      $("#promptField").show();
    } else {
      $("#promptField").hide();
    }
  });
});
