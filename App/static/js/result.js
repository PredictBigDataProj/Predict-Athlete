// DOM Content Loaded event handler
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

  // Flash messages fade out
  setTimeout(function () {
    let flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(function (msg) {
      msg.style.opacity = "0";
      setTimeout(() => (msg.style.display = "none"), 500);
    });
  }, 3000); // Messages disappear after 3 seconds
});

// Global navbar functions
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main-content").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main-content").style.marginLeft = "0";
}
