document.addEventListener("DOMContentLoaded", function () {
  var el = document.querySelector(".more");
  var btn = el.querySelector(".more-btn");
  var menu = el.querySelector(".more-menu");
  var visible = false;

  //  Function to Show Menu
  function showMenu(e) {
    e.preventDefault();
    if (!visible) {
      visible = true;
      el.classList.add("show-more-menu");
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
      el.classList.remove("show-more-menu");
      menu.setAttribute("aria-hidden", true);
      document.removeEventListener("mousedown", hideMenu);
    }
  }

  // Ensure Click Works for Profile Link
  document.querySelector(".more-menu a").addEventListener("click", function () {
    console.log("Profile link clicked! Navigating...");
    document.querySelector(".more-menu").classList.remove("show-more-menu");
    window.location.href = "/staff-profile";
  });

  btn.addEventListener("click", showMenu, false);

  //  Function to Open Sidebar Menu
  function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main-content").style.marginLeft = "250px";
  }

  //  Function to Close Sidebar Menu
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main-content").style.marginLeft = "0";
  }

  // Function to Filter Reviews in Search Bar
  function filterReviews() {
    let input, filter, reviews, studentName, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    reviews = document
      .getElementById("reviewsList")
      .getElementsByClassName("review-card");

    for (i = 0; i < reviews.length; i++) {
      studentName = reviews[i].querySelector("h4");

      if (studentName) {
        txtValue = studentName.textContent || studentName.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          reviews[i].style.display = "";
        } else {
          reviews[i].style.display = "none";
        }
      }
    }
  }

  //  Function to Search for Students
  function searchStudents() {
    const query = document.getElementById("searchQuery").value;

    fetch(`/searchStudent?query=${query}`)
      .then((response) => response.json())
      .then((data) => {
        const studentList = document.getElementById("student-list");
        const noStudentsMsg = document.getElementById("no-students");

        studentList.innerHTML = ""; // Clear existing students

        if (data.students.length > 0) {
          noStudentsMsg.style.display = "none";

          data.students.forEach((student) => {
            const card = document.createElement("div");
            card.classList.add("student-card");
            card.innerHTML = `
                        <h3>${student.firstname} ${student.lastname}</h3>
                        <p><strong>Student ID:</strong> ${student.UniId}</p>
                        <p><strong>Degree:</strong> ${
                          student.degree ? student.degree : "Not assigned"
                        }</p>
                        <a href="/getStudentProfile/${student.UniId}">
                            <button class="profile-button">View Profile</button>
                        </a>
                    `;
            studentList.appendChild(card);
          });
        } else {
          noStudentsMsg.style.display = "block";
        }
      })
      .catch((error) => console.error("Error fetching students:", error));
  }

  //  Attach Filter Function to Input Field
  document.getElementById("myInput").addEventListener("keyup", filterReviews);
});

//for navbar
// Sidenav Functions
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

// Document Ready Function
document.addEventListener("DOMContentLoaded", function () {
  // Define physical attributes
  const physicalAttrs = [
    "crossing",
    "finishing",
    "heading_accuracy",
    "short_passing",
    "volleys",
    "dribbling",
    "curve",
    "fk_accuracy",
    "long_passing",
    "ball_control",
    "acceleration",
    "sprint_speed",
    "agility",
    "reactions",
    "balance",
    "shot_power",
    "jumping",
    "stamina",
    "strength",
    "long_shots",
    "aggression",
    "interceptions",
    "positioning",
    "vision",
    "penalties",
    "composure",
    "defensive_awareness",
    "standing_tackle",
    "sliding_tackle",
    "gk_diving",
    "gk_handling",
    "gk_kicking",
    "gk_positioning",
    "gk_reflexes",
  ];

  // Get reasonable max from server (this value is passed from the template)
  const reasonableMax =
    parseInt(
      document.querySelector(".stats-container").dataset.reasonableMax
    ) || 2660;

  // Function to update total
  function updatePhysicalTotal() {
    let total = 0;
    physicalAttrs.forEach((attr) => {
      const slider = document.getElementById(attr);
      if (slider) {
        total += parseInt(slider.value || 0);
      }
    });

    // Update display
    const totalElement = document.getElementById("physical-total");
    if (totalElement) {
      totalElement.textContent = total;
    }

    // Show warning if exceeds reasonable max
    const warningElement = document.getElementById("validation-warning");
    if (warningElement) {
      if (total > reasonableMax) {
        warningElement.style.display = "block";
      } else {
        warningElement.style.display = "none";
      }
    }
  }

  // Add event listeners to all physical attribute sliders
  physicalAttrs.forEach((attr) => {
    const slider = document.getElementById(attr);
    const valueInput = document.getElementById(`${attr}_val`);

    if (slider) {
      slider.addEventListener("input", updatePhysicalTotal);

      // Sync number input with slider
      if (valueInput) {
        valueInput.addEventListener("input", function () {
          slider.value = this.value;
          updatePhysicalTotal();
        });
      }
    }
  });

  // Initial calculation
  updatePhysicalTotal();

  // Add form validation
  const form = document.getElementById("data-entry-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      let total = 0;
      physicalAttrs.forEach((attr) => {
        const slider = document.getElementById(attr);
        if (slider) {
          total += parseInt(slider.value || 0);
        }
      });

      if (total > reasonableMax) {
        event.preventDefault();
        alert(
          "Your physical attributes total exceeds realistic values. Please redistribute your points before submitting."
        );
      }
    });
  }

  // Stats expand/collapse functionality
  const expandBtn = document.getElementById("expand-stats");
  if (expandBtn) {
    expandBtn.addEventListener("click", function () {
      const statsCard = document.querySelector(".stats-card");
      const mainContent = document.querySelector(".main-content");

      // Create overlay if it doesn't exist
      let overlay = document.querySelector(".stats-overlay");
      if (!overlay) {
        overlay = document.createElement("div");
        overlay.className = "stats-overlay";
        document.body.appendChild(overlay);

        // Close expanded view when clicking overlay
        overlay.addEventListener("click", function () {
          statsCard.classList.remove("stats-expanded");
          overlay.style.display = "none";
          expandBtn.innerHTML = '<i class="fas fa-expand"></i>';
        });
      }

      // Toggle expanded state
      if (statsCard.classList.contains("stats-expanded")) {
        statsCard.classList.remove("stats-expanded");
        overlay.style.display = "none";
        expandBtn.innerHTML = '<i class="fas fa-expand"></i>';
      } else {
        statsCard.classList.add("stats-expanded");
        overlay.style.display = "block";
        expandBtn.innerHTML = '<i class="fas fa-compress"></i>';
      }
    });
  }

  // Handle responsive behavior for stats card
  function adjustStatsCardPosition() {
    const statsContainer = document.querySelector(".stats-container");
    if (!statsContainer) return;

    // On mobile (screen width less than 992px), remove sticky positioning
    if (window.innerWidth < 992) {
      statsContainer.style.position = "static";
    } else {
      statsContainer.style.position = "sticky";
    }
  }

  // Run on page load and window resize
  adjustStatsCardPosition();
  window.addEventListener("resize", adjustStatsCardPosition);
});
