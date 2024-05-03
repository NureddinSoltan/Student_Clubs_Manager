    function updateFilter(dropdownId, filterType, value, displayText) {
      let currentUrl = new URL(window.location.href);
      let searchParams = currentUrl.searchParams;
  
      // Update the search parameter based on the filter type and value
      if (value === 'all') {
          searchParams.delete(filterType); // Remove the parameter for 'all' selections
      } else {
          searchParams.set(filterType, value);
      }
  
      // Update the dropdown title to the selected option
      document.getElementById(dropdownId).textContent = displayText + ' ';
      const caretIcon = document.createElement('i');
      caretIcon.className = 'fa-solid fa-caret-down';
      document.getElementById(dropdownId).appendChild(caretIcon);
  
      // Redirect to the new URL with the updated parameters
      window.location.href = currentUrl.toString();
  }
  document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const type = urlParams.get('type');
    const status = urlParams.get('status');
    const order = urlParams.get('order');

    if (status) {
        const statusText = status.charAt(0).toUpperCase() + status.slice(1); // Capitalize the first letter
        updateDropdownTitle('filterByStatus', 'Filter by Status', statusText);
    }

    if (type) {
        const typeText = { 'event': 'Event Post', 'activity': 'Activity Form', 'edit': 'Edit Event Post' }[type] || 'All Types';
        updateDropdownTitle('filterByRequestTime', 'Filter by Request', typeText);
    }

    if (order) {
        const orderText = order === 'newest' ? 'Newest First' : 'Oldest';
        updateDropdownTitle('filterByDate', 'Filter by Time', orderText);
    }
});

function updateDropdownTitle(dropdownId, defaultText, newText) {
    const dropdown = document.getElementById(dropdownId);
    // Remove only the text node, keep the icon
    while (dropdown.firstChild && dropdown.firstChild.nodeType === Node.TEXT_NODE) {
        dropdown.removeChild(dropdown.firstChild);
    }
    // Add new text node
    dropdown.insertBefore(document.createTextNode(newText + ' '), dropdown.firstChild || null);
}
    function setActionType(action) {
      const modalLabel = document.getElementById('actionType');
      modalLabel.textContent = action;
      modalLabel.className = action; // Add the class for styling
      document.getElementById('confirmBtn').onclick = function () {
        console.log(action === 'accept' ? 'Accepted' : 'Rejected');
        var modalElement = document.getElementById('confirmationModal');
        var modalInstance = bootstrap.Modal.getInstance(modalElement);
        modalInstance.hide();
      };
    }