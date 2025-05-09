document.addEventListener("DOMContentLoaded", initializeApp);

let mostLikelyPosition;

function initializeApp() {
  initializeDataFromDOM();

  setupEventListeners();

  setupFlashMessages();

  animateRecommendation();
}

function initializeDataFromDOM() {
  const positionElement = document.getElementById("most-likely-position");

  if (positionElement) {
    mostLikelyPosition = positionElement.getAttribute("data-position");
  }
}

function setupEventListeners() {
  setupMenuListeners();

  setupSearchListeners();

  setupLeagueFitListeners();
}

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

function setupSearchListeners() {
  const searchInput = document.getElementById("myInput");
  if (searchInput) {
    searchInput.addEventListener("keyup", filterReviews);
  }
}


function setupLeagueFitListeners() {
  const openModalBtn = document.getElementById("open-modal-btn");

  if (openModalBtn) {
    openModalBtn.addEventListener("click", showLeagueFitModal);
  }
}

function showLeagueFitModal() {
  const countryList = document.getElementById("country-list");
  let countryOptions = "";

  if (countryList) {
    const options = countryList.querySelectorAll("option");
    options.forEach((option) => {
      if (option.value) {
        countryOptions += `<option value="${option.value}">${option.value}</option>`;
      }
    });
  }

  Swal.fire({
    title: "<strong>Find Your Best League Fit</strong>",
    icon: "info",
    html: `
      <div class="swal-form">
        <div class="swal-form-group">
          <label for="swal-country">Select your country:</label>
          <input list="swal-country-list" id="swal-country" class="swal2-input" placeholder="Start typing your country" required>
          <datalist id="swal-country-list">
            ${countryOptions}
          </datalist>
        </div>
        
        <div class="swal-form-group">
          <p>Preferred Foot:</p>
          <div class="swal-radio-group">
            <label><input type="radio" name="preferred_foot" value="Left"> Left</label>
            <label><input type="radio" name="preferred_foot" value="Right" checked> Right</label>
          </div>
        </div>
      </div>
    `,
    showCloseButton: true,
    showCancelButton: true,
    focusConfirm: false,
    confirmButtonText: `
      <i class="fa fa-paper-plane"></i> Submit
    `,
    confirmButtonAriaLabel: "Submit",
    cancelButtonText: `
      <i class="fa fa-times"></i> Cancel
    `,
    cancelButtonAriaLabel: "Cancel",
    preConfirm: () => {
      const country = document.getElementById("swal-country").value;
      const preferredFoot = document.querySelector(
        'input[name="preferred_foot"]:checked'
      ).value;

      if (!country) {
        Swal.showValidationMessage("Please select your country");
        return false;
      }

      return {
        country: country,
        preferredFoot: preferredFoot,
        careerLength: 0,
      };
    },
  }).then((result) => {
    if (result.isConfirmed) {
      const formData = result.value;
      handleLeagueFitSubmit(formData);
    }
  });
}


function handleLeagueFitSubmit(formData) {
  const leagueFitResult = document.getElementById("league-fit-result");

  if (!leagueFitResult) return;

  const requestData = {
    attributes: inputData,
    country: formData.country,
    career_length: 0,
    preferred_foot: formData.preferredFoot,
    position: mostLikelyPosition,
  };

  Swal.fire({
    title: "Finding best leagues...",
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    },
  });

  fetchLeagueFit(requestData, leagueFitResult);
}

function fetchLeagueFit(requestData, resultElement) {
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
      Swal.close();

      displayLeagueFitResults(data, resultElement);

      Swal.fire({
        title: "Success!",
        text: "We found your best league matches!",
        icon: "success",
        timer: 2000,
        showConfirmButton: false,
      });
    })
    .catch((error) => {
      console.error("Error fetching league fit data:", error);

      Swal.close();

      Swal.fire({
        title: "Error!",
        text: "Failed to fetch league data. Please try again.",
        icon: "error",
      });

      resultElement.innerHTML =
        '<p class="error">Error fetching league data. Please try again.</p>';
    });
}

function displayLeagueFitResults(data, resultElement) {
  if (!data.top_leagues || !data.top_leagues.length) {
    resultElement.innerHTML = "<p>No league recommendations available.</p>";
    return;
  }

  let resultHTML = `
    <div class="league-results">

      <h3>Top 3 League Fits</h3>
      <div class="league-list">
  `;

  data.top_leagues.forEach((entry, index) => {
    const medal = index === 0 ? "1" : index === 1 ? "2" : "3";
    resultHTML += `
      <div class="league-item">
        <span class="league-medal">${medal}</span>
        <span class="league-name">${entry.league}</span>
        <span class="league-score">Score: ${entry.score.toFixed(2)} / 39.0</span>
      </div>
    `;
  });

  resultHTML += `
      </div>
    </div>
  `;

  resultElement.innerHTML = resultHTML;
}

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

function animateRecommendation() {
  if (typeof anime === "undefined") {
    console.error("anime.js is not loaded!");
    return;
  }

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

  animatePositionItems();

  animatePlayerItems();
}

function animateElement(selector, config) {
  const element = document.querySelector(selector);
  if (!element) return;

  if (config.initialStyles) {
    Object.assign(element.style, config.initialStyles);
  }

  anime({
    targets: selector,
    ...config.animation,
  });
}

function animatePositionItems() {
  const positionItems = document.querySelectorAll(".position-item");
  if (!positionItems.length) return;

  positionItems.forEach((item, index) => {
    const percentage = parseFloat(item.getAttribute("data-percentage") || "0");

    if (percentage < 1) {
      item.classList.add("very-low-probability");
      return;
    }

    item.style.opacity = "0";
    item.style.transform = "translateX(-20px)";

    anime({
      targets: item,
      opacity: [0, 1],
      translateX: [-20, 0],
      easing: "easeOutExpo",
      duration: 800,
      delay: 2000 + index * 100,
    });

    const bar = item.querySelector(".position-bar");
    if (bar) {
      createColoredBarFill(bar, percentage);
    }
  });
}

function createColoredBarFill(barElement, percentage) {
  const barFill = document.createElement("div");
  barFill.className = "position-bar-fill";

  if (percentage >= 60) {
    barFill.classList.add("probability-high");
  } else if (percentage >= 30) {
    barFill.classList.add("probability-medium");
  } else {
    barFill.classList.add("probability-low");
  }

  barElement.appendChild(barFill);

  anime({
    targets: barFill,
    width: percentage + "%",
    easing: "easeInOutQuart",
    duration: 1000,
    delay: 200,
  });
}

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

function openNav() {
  const sidenav = document.getElementById("mySidenav");
  const mainContent = document.getElementById("main-content");

  if (sidenav) sidenav.style.width = "250px";
  if (mainContent) mainContent.style.marginLeft = "250px";
}

function closeNav() {
  const sidenav = document.getElementById("mySidenav");
  const mainContent = document.getElementById("main-content");

  if (sidenav) sidenav.style.width = "0";
  if (mainContent) mainContent.style.marginLeft = "0";
}
