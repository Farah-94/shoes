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



// ---------------buy_product-------------------



document.addEventListener('DOMContentLoaded', () => {
  console.log('🥾 script loaded, DOM ready');

  const slider  = document.querySelector('.product-slider');
  console.log('🥾 Found .product-slider?', !!slider);
  if (!slider) return;

  const slides  = Array.from(slider.querySelectorAll('.slide'));
  const prevBtn = slider.querySelector('.prev');
  const nextBtn = slider.querySelector('.next');
  let   current = 0;

  console.log(`🥾 slides: ${slides.length}`, slides);
  console.log(`🥾 prevBtn?`, prevBtn, `nextBtn?`, nextBtn);

  const showSlide = i => {
    console.log('🥾 showSlide(', i, ')');
    slides.forEach((s, idx) => {
      s.style.display = idx === i ? 'block' : 'none';
    });
  };

  const nextSlide = () => {
    console.log('🥾 nextSlide clicked');
    current = (current + 1) % slides.length;
    showSlide(current);
  };
  const prevSlide = () => {
    console.log('🥾 prevSlide clicked');
    current = (current - 1 + slides.length) % slides.length;
    showSlide(current);
  };

  if (slides.length) {
    showSlide(current);
    if (slides.length > 1) {
      console.log('🥾 Attaching click handlers');
      nextBtn?.addEventListener('click', nextSlide);
      prevBtn?.addEventListener('click', prevSlide);
    }
  }


  // Click-to-zoom: open whatever slide you click in a new tab
  slides.forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => window.open(img.src, '_blank'));
  });
});



