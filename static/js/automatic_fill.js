document.getElementById('confirmSubmit').addEventListener('click', function() {
  document.querySelector('form').submit();
});


// function updatePresidentInfo() {
//   var selectedManager = document.getElementById('managers');
//   var firstName = selectedManager.options[selectedManager.selectedIndex].getAttribute('data-first-name');
//   var lastName = selectedManager.options[selectedManager.selectedIndex].getAttribute('data-last-name');
//   document.getElementById('presidentFirstName').value = firstName;
//   document.getElementById('presidentLastName').value = lastName;
// }
function updatePresidentInfo() {
  var selectedManager = document.getElementById('managers');
  var firstName = selectedManager.options[selectedManager.selectedIndex].getAttribute('data-first-name');
  var lastName = selectedManager.options[selectedManager.selectedIndex].getAttribute('data-last-name');
  document.getElementById('presidentFirstName').value = firstName;
  document.getElementById('presidentLastName').value = lastName;
}