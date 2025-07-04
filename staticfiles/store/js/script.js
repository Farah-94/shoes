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


   
  document.getElementById("contactForm").addEventListener("submit", function(e) {
    e.preventDefault(); // Prevent the default form submission.

    const form = this;
    const formData = new FormData(form);

    fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        Accept: "application/json"
      }
    })
    .then(response => {
      if (response.ok) {
        alert("Thanks for your message!");
        form.reset(); // Clear the form on success.
      } else {
        response.json().then(data => {
          if (Object.hasOwn(data, 'errors')) {
            alert("Oops! " + data["errors"].map(error => error["message"]).join(", "));
          } else {
            alert("Oops! There was a problem submitting your form");
          }
        });
      }
    })
    .catch(error => {
      console.error("Error submitting form:", error);
      alert("Oops! There was a problem submitting your form");
    });
  });
