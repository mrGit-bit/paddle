// paddle/frontend/static/frontend/js/tabPaginationReset.js
document.addEventListener("DOMContentLoaded", function () {
  console.log("Document loaded. Setting up tab-based pagination toggle...");

  // Cache references to the tab elements
  const userTab = document.getElementById("user-matches-tab");
  const allTab = document.getElementById("all-matches-tab");

  // Cache references to the pagination elements
  const userPagination = document.getElementById("user-pagination");
  const allPagination = document.getElementById("all-pagination");
  
  // Cache references to the tab panes
  const userTabPane = document.getElementById("user-matches");
  const allTabPane = document.getElementById("all-matches");
  // Function to show pagination based on the active tab
  function showPaginationForActiveTab() {
    console.log("Checking which tab is active...");

    if (userTabPane.classList.contains("active", "show")) {
      console.log("User Matches tab is active. Showing user pagination.");
      userPagination.style.display = "block";
      allPagination.style.display = "none";
    } else if (allTabPane.classList.contains("active", "show")) {
      console.log("All Matches tab is active. Showing all pagination.");
      allPagination.style.display = "block";
      userPagination.style.display = "none";
    }
  }

  // ✅ On initial load, check the URL hash and activate the correct tab
  const initialHash = window.location.hash;
  if (initialHash === "#all-matches") {
    console.log("Initial hash is #all-matches, switching tab...");
    const allTabTrigger = new bootstrap.Tab(allTab);
    allTabTrigger.show();
  } else {
    // Defaults to user matches (already active in markup)
    console.log("Defaulting to My Matches tab.");
  }

  // Execute on page load to set the correct pagination
  showPaginationForActiveTab();

  // Add event listeners to tabs to toggle pagination on tab change
  const tabTriggers = document.querySelectorAll('a[data-bs-toggle="tab"]');
  tabTriggers.forEach(tab => {
    tab.addEventListener("shown.bs.tab", () => {
      console.log("Tab changed. Re-checking active tab for pagination...");
      showPaginationForActiveTab();

      // Reset pagination to page 1 on tab switch
      const targetTabId = tab.getAttribute("href"); // Get the target tab's ID "#user-matches" or "#all-matches"
      console.log(`Switching to tab ${targetTabId}, resetting to page 1`);

      // Use window.location.origin + path to avoid adding duplicate anchors
      const baseUrl = window.location.origin + window.location.pathname;
      window.location.href = `${baseUrl}?page=1${targetTabId}`;
    });
  });
});

