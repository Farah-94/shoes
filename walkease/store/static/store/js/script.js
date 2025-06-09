document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".slide");
  let currentSlide = 0;
  const slideInterval = setInterval(nextSlide, 3000); // changes slide every 3 seconds

  function nextSlide() {
    slides[currentSlide].classList.remove("active");
    currentSlide = (currentSlide + 1) % slides.length;
    slides[currentSlide].classList.add("active");
  }
});


document.addEventListener("DOMContentLoaded", function() {
      const menuButton = document.getElementById("menu-button");
      const menuDropdown = document.getElementById("menu-dropdown");

      menuButton.addEventListener("click", function(event) {
        event.stopPropagation(); // Prevent the click from propagating to the window
        menuDropdown.classList.toggle("show");
      });

      // Optional: Hide dropdown when clicking anywhere outside the menu
      window.addEventListener("click", function() {
        if (menuDropdown.classList.contains("show")) {
          menuDropdown.classList.remove("show");
        }
      });
    });
