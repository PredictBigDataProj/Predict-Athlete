// Main initialization function
document.addEventListener("DOMContentLoaded", initializeApp);

// Global variables
let inputData, mostLikelyPosition;

/**
 * Initialize the application
 */
function initializeApp() {
  // Initialize data from HTML
  initializeDataFromDOM();

  // Set up UI event listeners
  setupEventListeners();

  // Handle flash messages
  setupFlashMessages();

  // Start animations
  animateRecommendation();
}

/**
 * Initialize data from DOM elements
 */
function initializeDataFromDOM() {
  const inputDataElement = document.getElementById("input-data");
  const positionElement = document.getElementById("most-likely-position");

  if (inputDataElement) {
    try {
      inputData = JSON.parse(inputDataElement.getAttribute("data-input"));
    } catch (error) {
      console.error("Error parsing input data:", error);
    }
  }

  if (positionElement) {
    mostLikelyPosition = positionElement.getAttribute("data-position");
  }
}

/**
 * Set up all event listeners
 */
function setupEventListeners() {
  // Menu functionality
  setupMenuListeners();

  // Search functionality
  setupSearchListeners();

  // League fit modal functionality
  setupLeagueFitListeners();
}

/**
 * Set up menu-related event listeners
 */
function setupMenuListeners() {
  const moreEl = document.querySelector(".more");
  if (!moreEl) return;

  const btn = moreEl.querySelector(".more-btn");
  const menu = moreEl.querySelector(".more-menu");
  let visible = false;

  if (btn) {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      if (!visible) {
        visible = true;
        moreEl.classList.add("show-more-menu");
        menu.setAttribute("aria-hidden", false);
        document.addEventListener("mousedown", handleMenuOutsideClick);
      }
    });
  }

  const profileLink = document.querySelector(".more-menu a");
  if (profileLink) {
    profileLink.addEventListener("click", () => {
      console.log("Profile link clicked! Navigating...");
      document.querySelector(".more-menu").classList.remove("show-more-menu");
      window.location.href = "/staff-profile";
    });
  }

  function handleMenuOutsideClick(e) {
    if (btn.contains(e.target) || menu.contains(e.target)) return;

    if (visible) {
      visible = false;
      moreEl.classList.remove("show-more-menu");
      menu.setAttribute("aria-hidden", true);
      document.removeEventListener("mousedown", handleMenuOutsideClick);
    }
  }
}

/**
 * Set up search functionality
 */
function setupSearchListeners() {
  const searchInput = document.getElementById("myInput");
  if (searchInput) {
    searchInput.addEventListener("keyup", filterReviews);
  }
}

/**
 * Set up league fit modal listeners
 */
function setupLeagueFitListeners() {
  const openModalBtn = document.getElementById("open-modal-btn");
  const closeModalBtn = document.getElementById("close-modal");
  const submitModalBtn = document.getElementById("submit-modal");
  const leagueModal = document.getElementById("league-modal");

  if (openModalBtn) {
    openModalBtn.addEventListener("click", () => {
      if (leagueModal) leagueModal.style.display = "block";
    });
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", () => {
      if (leagueModal) leagueModal.style.display = "none";
    });
  }

  if (submitModalBtn) {
    submitModalBtn.addEventListener("click", handleLeagueFitSubmit);
  }
}

/**
 * Handle league fit form submission
 */
function handleLeagueFitSubmit() {
  const countryInput = document.getElementById("country");
  const preferredFootInputs = document.querySelectorAll(
    'input[name="preferred_foot"]'
  );
  const careerLengthInput = document.getElementById("career_length");
  const leagueFitResult = document.getElementById("league-fit-result");
  const leagueModal = document.getElementById("league-modal");

  if (!countryInput || !careerLengthInput || !leagueFitResult) return;

  const country = countryInput.value;
  const careerLength = careerLengthInput.value;

  let preferredFoot = "Right"; // Default
  for (const input of preferredFootInputs) {
    if (input.checked) {
      preferredFoot = input.value;
      break;
    }
  }

  if (!country || !careerLength) {
    alert("Please fill out all fields.");
    return;
  }

  const requestData = {
    attributes: inputData,
    country: country,
    career_length: parseInt(careerLength),
    preferred_foot: preferredFoot,
    position: mostLikelyPosition,
  };

  fetchLeagueFit(requestData, leagueFitResult, leagueModal);
}

/**
 * Fetch league fit data from server
 */
function fetchLeagueFit(requestData, resultElement, modalElement) {
  fetch("/best-fit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      displayLeagueFitResults(data, resultElement);
      if (modalElement) modalElement.style.display = "none";
    })
    .catch((error) => {
      console.error("Error fetching league fit data:", error);
      resultElement.innerHTML =
        '<p class="error">Error fetching league data. Please try again.</p>';
    });
}

/**
 * Display league fit results
 */
function displayLeagueFitResults(data, resultElement) {
  if (!data.top_leagues || !data.top_leagues.length) {
    resultElement.innerHTML = "<p>No league recommendations available.</p>";
    return;
  }

  let resultHTML = "<h4>Top 3 League Fits:</h4><ol>";
  data.top_leagues.forEach((entry) => {
    resultHTML += `<li>${entry.league} (Score: ${entry.score.toFixed(2)})</li>`;
  });
  resultHTML += "</ol>";
  resultElement.innerHTML = resultHTML;
}

/**
 * Set up flash messages
 */
function setupFlashMessages() {
  const flashMessages = document.querySelectorAll(".flash-message");
  if (!flashMessages.length) return;

  setTimeout(() => {
    flashMessages.forEach((msg) => {
      msg.style.opacity = "0";
      setTimeout(() => (msg.style.display = "none"), 500);
    });
  }, 3000);
}

/**
 * Filter reviews based on search input
 */
function filterReviews() {
  const input = document.getElementById("myInput");
  if (!input) return;

  const filter = input.value.toUpperCase();
  const reviews = document.getElementById("reviewsList");
  if (!reviews) return;

  const reviewCards = reviews.getElementsByClassName("review-card");

  for (let i = 0; i < reviewCards.length; i++) {
    const studentName = reviewCards[i].querySelector("h4");

    if (studentName) {
      const txtValue = studentName.textContent || studentName.innerText;
      reviewCards[i].style.display =
        txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none";
    }
  }
}

/**
 * Animate recommendation elements
 */
function animateRecommendation() {
  if (typeof anime === "undefined") {
    console.error("anime.js is not loaded!");
    return;
  }

  // Animate position card
  animateElement(".position-card", {
    initialStyles: { opacity: "0", transform: "translateY(20px)" },
    animation: {
      opacity: [0, 1],
      translateY: [20, 0],
      easing: "easeOutExpo",
      duration: 1000,
      delay: 300,
    },
  });

  // Animate position name
  animateElement(".position-name", {
    initialStyles: { opacity: "0", transform: "scale(0.8)" },
    animation: {
      opacity: [0, 1],
      scale: [0.8, 1],
      easing: "easeOutElastic(1, .5)",
      duration: 1500,
      delay: 800,
    },
  });

  // Animate compatibility fill
  const compatibilityFill = document.querySelector(".compatibility-fill");
  if (compatibilityFill) {
    const percentage = parseInt(
      compatibilityFill.getAttribute("data-percentage") || "0"
    );
    compatibilityFill.style.width = "0%";

    anime({
      targets: ".compatibility-fill",
      width: percentage + "%",
      easing: "easeInOutQuart",
      duration: 1500,
      delay: 1200,
    });
  }

  // Animate compatibility text
  animateElement(".compatibility-text", {
    initialStyles: { opacity: "0", transform: "translateY(10px)" },
    animation: {
      opacity: [0, 1],
      translateY: [10, 0],
      easing: "easeOutExpo",
      duration: 800,
      delay: 1800,
    },
  });

  // Animate position items
  animatePositionItems();

  // Animate player items
  animatePlayerItems();
}

/**
 * Helper function to animate an element
 */
function animateElement(selector, config) {
  const element = document.querySelector(selector);
  if (!element) return;

  // Apply initial styles
  if (config.initialStyles) {
    Object.assign(element.style, config.initialStyles);
  }

  // Apply animation
  anime({
    targets: selector,
    ...config.animation,
  });
}

/**
 * Animate position items with color-coded bars
 */
function animatePositionItems() {
  const positionItems = document.querySelectorAll(".position-item");
  if (!positionItems.length) return;

  positionItems.forEach((item, index) => {
    const percentage = parseFloat(item.getAttribute("data-percentage") || "0");

    // Hide very low probabilities
    if (percentage < 1) {
      item.classList.add("very-low-probability");
      return;
    }

    // Set initial styles
    item.style.opacity = "0";
    item.style.transform = "translateX(-20px)";

    // Animate the item
    anime({
      targets: item,
      opacity: [0, 1],
      translateX: [-20, 0],
      easing: "easeOutExpo",
      duration: 800,
      delay: 2000 + index * 100,
    });

    // Create and animate the bar fill
    const bar = item.querySelector(".position-bar");
    if (bar) {
      createColoredBarFill(bar, percentage);
    }
  });
}

/**
 * Create a colored bar fill based on percentage
 */
function createColoredBarFill(barElement, percentage) {
  const barFill = document.createElement("div");
  barFill.className = "position-bar-fill";

  // Add appropriate color class based on percentage
  if (percentage >= 60) {
    barFill.classList.add("probability-high");
  } else if (percentage >= 30) {
    barFill.classList.add("probability-medium");
  } else {
    barFill.classList.add("probability-low");
  }

  barElement.appendChild(barFill);

  // Animate the bar fill
  anime({
    targets: barFill,
    width: percentage + "%",
    easing: "easeInOutQuart",
    duration: 1000,
    delay: 200,
  });
}

/**
 * Animate player items
 */
function animatePlayerItems() {
  const playerItems = document.querySelectorAll(".player-item");
  if (!playerItems.length) return;

  playerItems.forEach((item, index) => {
    item.style.opacity = "0";
    item.style.transform = "translateX(-20px)";

    anime({
      targets: item,
      opacity: [0, 1],
      translateX: [-20, 0],
      easing: "easeOutExpo",
      duration: 800,
      delay: 2500 + index * 100,
    });
  });
}

/**
 * Open navigation sidebar
 */
function openNav() {
  const sidenav = document.getElementById("mySidenav");
  const mainContent = document.getElementById("main-content");

  if (sidenav) sidenav.style.width = "250px";
  if (mainContent) mainContent.style.marginLeft = "250px";
}

/**
 * Close navigation sidebar
 */
function closeNav() {
  const sidenav = document.getElementById("mySidenav");
  const mainContent = document.getElementById("main-content");

  if (sidenav) sidenav.style.width = "0";
  if (mainContent) mainContent.style.marginLeft = "0";
}
