document.addEventListener("DOMContentLoaded", function () {
  var el = document.querySelector(".more");
  var btn = el.querySelector(".more-btn");
  var menu = el.querySelector(".more-menu");
  var visible = false;

  function showMenu(e) {
    e.preventDefault();
    if (!visible) {
      visible = true;
      el.classList.add("show-more-menu");
      menu.setAttribute("aria-hidden", false);
      document.addEventListener("mousedown", hideMenu, false);
    }
  }

  function hideMenu(e) {
    if (btn.contains(e.target) || menu.contains(e.target)) {
      return;
    }
    if (visible) {
      visible = false;
      el.classList.remove("show-more-menu");
      menu.setAttribute("aria-hidden", true);
      document.removeEventListener("mousedown", hideMenu);
    }
  }

  document.querySelector(".more-menu a").addEventListener("click", function () {
    console.log("Profile link clicked! Navigating...");
    document.querySelector(".more-menu").classList.remove("show-more-menu");
    window.location.href = "/staff-profile";
  });

  btn.addEventListener("click", showMenu, false);

  function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main-content").style.marginLeft = "250px";
  }

  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main-content").style.marginLeft = "0";
  }

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

  document.getElementById("myInput").addEventListener("keyup", filterReviews);
});

document.addEventListener("DOMContentLoaded", function () {

  // Sidenav functionality
  window.openNav = function () {
    document.getElementById("mySidenav").style.width = "250px";
  };

  window.closeNav = function () {
    document.getElementById("mySidenav").style.width = "0";
  };



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

  const reasonableMax =
    parseInt(
      document.querySelector(".stats-container")?.dataset.reasonableMax
    ) || 2660;

  function updatePhysicalTotal() {
    let total = 0;
    physicalAttrs.forEach((attr) => {
      const slider = document.getElementById(attr);
      if (slider) {
        total += parseInt(slider.value || 0);
      }
    });

    const totalElement = document.getElementById("physical-total");
    if (totalElement) {
      totalElement.textContent = total;
    }

    const warningElement = document.getElementById("validation-warning");
    if (warningElement) {
      if (total > reasonableMax) {
        warningElement.style.display = "block";
      } else {
        warningElement.style.display = "none";
      }
    }
  }

  physicalAttrs.forEach((attr) => {
    const slider = document.getElementById(attr);
    const valueInput = document.getElementById(`${attr}_val`);

    if (slider) {
      slider.addEventListener("input", updatePhysicalTotal);

      if (valueInput) {
        valueInput.addEventListener("input", function () {
          slider.value = this.value;
          updatePhysicalTotal();
        });
      }
    }
  });

  updatePhysicalTotal();

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

  const expandBtn = document.getElementById("expand-stats");
  if (expandBtn) {
    expandBtn.addEventListener("click", function () {
      const statsCard = document.querySelector(".stats-card");

      let overlay = document.querySelector(".stats-overlay");
      if (!overlay) {
        overlay = document.createElement("div");
        overlay.className = "stats-overlay";
        document.body.appendChild(overlay);

        overlay.addEventListener("click", function () {
          statsCard.classList.remove("stats-expanded");
          overlay.style.display = "none";
          expandBtn.innerHTML = '<i class="fas fa-expand"></i>';
        });
      }

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

  // Add toggle stats button for mobile
  function setupMobileStatsToggle() {
    const mainContent = document.querySelector('.main-content');
    const statsContainer = document.querySelector('.stats-container');
    
    if (!mainContent || !statsContainer) return;
    
    // Create toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'toggle-stats-btn';
    toggleBtn.innerHTML = '<i class="fas fa-chart-bar"></i> Show Stats';
    toggleBtn.setAttribute('type', 'button');
    
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'mobile-stats-overlay';
    document.body.appendChild(overlay);
    
    // Insert button after form container
    const formContainer = document.querySelector('.form-container');
    if (formContainer) {
      formContainer.insertAdjacentElement('afterend', toggleBtn);
    } else {
      mainContent.insertBefore(toggleBtn, statsContainer);
    }
    
    // Toggle functionality
    toggleBtn.addEventListener('click', function() {
      statsContainer.classList.add('mobile-visible');
      overlay.style.display = 'block';
      
      // Add close button to stats card
      const closeBtn = document.createElement('button');
      closeBtn.className = 'close-stats-btn';
      closeBtn.innerHTML = '<i class="fas fa-times"></i>';
      closeBtn.style.position = 'absolute';
      closeBtn.style.top = '10px';
      closeBtn.style.right = '10px';
      closeBtn.style.background = 'none';
      closeBtn.style.border = 'none';
      closeBtn.style.color = 'white';
      closeBtn.style.fontSize = '20px';
      closeBtn.style.cursor = 'pointer';
      
      const cardHeader = statsContainer.querySelector('.card-header');
      if (cardHeader && !cardHeader.querySelector('.close-stats-btn')) {
        cardHeader.appendChild(closeBtn);
      }
      
      // Close functionality
      function closeStats() {
        statsContainer.classList.remove('mobile-visible');
        overlay.style.display = 'none';
      }
      
      closeBtn.addEventListener('click', closeStats);
      overlay.addEventListener('click', closeStats);
    });
  }
  
  setupMobileStatsToggle();
  window.addEventListener("resize", adjustStatsCardPosition);
});

// Moved openNav and closeNav functions outside to avoid duplication
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

// Sample player data function - kept as it's used by the Load Mbappe Data button
function loadTestPlayerData() {
  const SampleData = {
    height_cm: 182,
    weight_kg: 75,
    crossing: 78,
    finishing: 94,
    heading_accuracy: 73,
    short_passing: 86,
    volleys: 84,
    dribbling: 93,
    curve: 80,
    fk_accuracy: 69,
    long_passing: 71,
    ball_control: 92,
    acceleration: 97,
    sprint_speed: 97,
    agility: 93,
    reactions: 93,
    balance: 82,
    shot_power: 90,
    jumping: 88,
    stamina: 88,
    strength: 77,
    long_shots: 83,
    aggression: 64,
    interceptions: 38,
    positioning: 93,
    vision: 83,
    penalties: 84,
    composure: 88,
    defensive_awareness: 26,
    standing_tackle: 34,
    sliding_tackle: 32,
    gk_diving: 13,
    gk_handling: 5,
    gk_kicking: 7,
    gk_positioning: 11,
    gk_reflexes: 6,
    age: 26,
  };

  for (const attr in SampleData) {
    const rangeInput = document.getElementById(attr);
    const numberInput = document.getElementById(attr + "_val");
    if (rangeInput && numberInput) {
      rangeInput.value = SampleData[attr];
      numberInput.value = SampleData[attr];
    }
  }

  // Trigger update of physical total after loading data
  document.dispatchEvent(new Event("DOMContentLoaded"));
}
