// profileDropdown.js

$(document).ready(function() {
  // Toggle profile-info when profileLink is clicked
  $('#profileLink').click(function() {
    $('.profile-info').toggle();
  });

  // Hide profile-info when clicking outside
  $(document).click(function(event) {
    // Check if the clicked element is not within the profile dropdown
    if (!$(event.target).closest('.profile-dropdown').length) {
      // Hide the profile dropdown
      $('.profile-info').hide();
    }
  });

  // Prevent clicks inside profile dropdown from closing it
  $('.profile-info').click(function(event) {
    event.stopPropagation();
  });
});
