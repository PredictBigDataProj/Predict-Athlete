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

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

document.addEventListener("DOMContentLoaded", function () {
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
      document.querySelector(".stats-container").dataset.reasonableMax
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
      const mainContent = document.querySelector(".main-content");

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

  function adjustStatsCardPosition() {
    const statsContainer = document.querySelector(".stats-container");
    if (!statsContainer) return;

    if (window.innerWidth < 992) {
      statsContainer.style.position = "static";
    } else {
      statsContainer.style.position = "sticky";
    }
  }

  adjustStatsCardPosition();
  window.addEventListener("resize", adjustStatsCardPosition);
});
