document.addEventListener("DOMContentLoaded", function () {
  // Check if elements exist before trying to access them
  const moreEl = document.querySelector(".more");
  if (moreEl) {
    var btn = moreEl.querySelector(".more-btn");
    var menu = moreEl.querySelector(".more-menu");
    var visible = false;

    //  Function to Show Menu
    function showMenu(e) {
      e.preventDefault();
      if (!visible) {
        visible = true;
        moreEl.classList.add("show-more-menu");
        menu.setAttribute("aria-hidden", false);
        document.addEventListener("mousedown", hideMenu, false);
      }
    }

    //  Function to Hide Menu When Clicking Outside
    function hideMenu(e) {
      if (btn.contains(e.target) || menu.contains(e.target)) {
        return; // Don't close if clicking inside the menu
      }
      if (visible) {
        visible = false;
        moreEl.classList.remove("show-more-menu");
        menu.setAttribute("aria-hidden", true);
        document.removeEventListener("mousedown", hideMenu);
      }
    }

    // Add event listener only if elements exist
    if (btn) {
      btn.addEventListener("click", showMenu, false);
    }

    // Ensure Click Works for Profile Link
    const profileLink = document.querySelector(".more-menu a");
    if (profileLink) {
      profileLink.addEventListener("click", function () {
        console.log("Profile link clicked! Navigating...");
        document.querySelector(".more-menu").classList.remove("show-more-menu");
        window.location.href = "/staff-profile";
      });
    }
  }

  // Flash messages fade out
  setTimeout(function () {
    let flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(function (msg) {
      msg.style.opacity = "0";
      setTimeout(() => (msg.style.display = "none"), 500);
    });
  }, 3000); // Messages disappear after 3 seconds

  // Position recommendation animations - call this function directly
  animateRecommendation();
});

// Global navbar functions
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

function animateRecommendation() {
  console.log("Animation function called");

  if (typeof anime === "undefined") {
    console.error("anime.js is not loaded!");
    return;
  }

  const positionCard = document.querySelector(".position-card");
  if (positionCard) {
    console.log("Animating position card");
    positionCard.style.opacity = "0";
    positionCard.style.transform = "translateY(20px)";

    anime({
      targets: ".position-card",
      opacity: [0, 1],
      translateY: [20, 0],
      easing: "easeOutExpo",
      duration: 1000,
      delay: 300,
    });
  }

  const positionName = document.querySelector(".position-name");
  if (positionName) {
    console.log("Animating position name");
    positionName.style.opacity = "0";
    positionName.style.transform = "scale(0.8)";

    anime({
      targets: ".position-name",
      opacity: [0, 1],
      scale: [0.8, 1],
      easing: "easeOutElastic(1, .5)",
      duration: 1500,
      delay: 800,
    });
  }

  const compatibilityFill = document.querySelector(".compatibility-fill");
  if (compatibilityFill) {
    console.log("Animating compatibility bar");
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

  const compatibilityText = document.querySelector(".compatibility-text");
  if (compatibilityText) {
    console.log("Animating compatibility text");
    compatibilityText.style.opacity = "0";
    compatibilityText.style.transform = "translateY(10px)";

    anime({
      targets: ".compatibility-text",
      opacity: [0, 1],
      translateY: [10, 0],
      easing: "easeOutExpo",
      duration: 800,
      delay: 1800,
    });
  }

  const positionItems = document.querySelectorAll(".position-item");
  if (positionItems.length) {
    console.log(`Animating ${positionItems.length} position items`);

    positionItems.forEach((item, index) => {
      const percentage = parseFloat(
        item.getAttribute("data-percentage") || "0"
      );

      if (percentage < 1) {
        item.classList.add("very-low-probability");
      }

      item.style.opacity = "0";
      item.style.transform = "translateX(-20px)";
      const bar = item.querySelector(".position-bar");

      anime({
        targets: item,
        opacity: [0, 1],
        translateX: [-20, 0],
        easing: "easeOutExpo",
        duration: 800,
        delay: 2000 + index * 100,
      });

      if (bar) {
        const barFill = document.createElement("div");
        barFill.className = "position-bar-fill";

        if (percentage >= 60) {
          barFill.classList.add("probability-high");
        } else if (percentage >= 30) {
          barFill.classList.add("probability-medium");
        } else {
          barFill.classList.add("probability-low");
        }

        bar.appendChild(barFill);

        anime({
          targets: barFill,
          width: percentage + "%",
          easing: "easeInOutQuart",
          duration: 1000,
          delay: 2200 + index * 100,
        });
      }
    });
  }

  const playerItems = document.querySelectorAll(".player-item");
  if (playerItems.length) {
    console.log(`Animating ${playerItems.length} player items`);

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
}

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("myInput");
  if (searchInput) {
    searchInput.addEventListener("keyup", filterReviews);
  }
});
