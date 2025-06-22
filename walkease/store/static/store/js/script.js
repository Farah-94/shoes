// static/store/js/script.js

document.addEventListener('DOMContentLoaded', () => {
  // 1) AUTO-ROTATING BANNER SLIDER (index.html)
  const bannerContainer = document.querySelector('.slider-container');
  if (bannerContainer) {
    const bannerSlides = Array.from(bannerContainer.querySelectorAll('.slide'));
    let bannerIndex = 0;
    // show only the first slide
    bannerSlides.forEach((s, i) => s.classList.toggle('active', i === 0));
    setInterval(() => {
      bannerSlides[bannerIndex].classList.remove('active');
      bannerIndex = (bannerIndex + 1) % bannerSlides.length;
      bannerSlides[bannerIndex].classList.add('active');
    }, 3000);
  }

  // 2) MENU DROPDOWN TOGGLE
  const menuButton   = document.getElementById('menu-button');
  const menuDropdown = document.getElementById('menu-dropdown');
  if (menuButton && menuDropdown) {
    menuButton.addEventListener('click', e => {
      e.stopPropagation();
      menuDropdown.classList.toggle('show');
    });
    window.addEventListener('click', () => {
      menuDropdown.classList.remove('show');
    });
  }

  // 3) CONTACT FORM AJAX SUBMISSION
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', e => {
      e.preventDefault();
      const formData = new FormData(contactForm);
      fetch(contactForm.action, {
        method: 'POST',
        body: formData,
        headers: { Accept: 'application/json' }
      })
      .then(res => {
        if (res.ok) {
          alert('Thanks for your message!');
          contactForm.reset();
        } else {
          return res.json().then(data => {
            const msg = data.errors
              ? data.errors.map(err => err.message).join(', ')
              : 'There was a problem submitting your form';
            alert('Oops! ' + msg);
          });
        }
      })
      .catch(() => alert('Oops! There was a problem submitting your form'));
    });
  }

  // 4) PRODUCT IMAGE SLIDER (buy_product.html)
  const productSlider = document.querySelector('.product-slider');
  if (productSlider) {
    const slides  = Array.from(productSlider.querySelectorAll('.slide'));
    const prevBtn = productSlider.querySelector('.prev');
    const nextBtn = productSlider.querySelector('.next');
    let   current = 0;

    // hide all except the first slide
    slides.forEach((s, i) => {
      s.style.display = i === 0 ? 'block' : 'none';
    });

    const showSlide = idx => {
      slides.forEach((s, i) => {
        s.style.display = i === idx ? 'block' : 'none';
      });
    };

    if (slides.length > 1) {
      nextBtn?.addEventListener('click', () => {
        current = (current + 1) % slides.length;
        showSlide(current);
      });
      prevBtn?.addEventListener('click', () => {
        current = (current - 1 + slides.length) % slides.length;
        showSlide(current);
      });
    }

    // click-to-zoom behavior
    slides.forEach(img => {
      img.style.cursor = 'zoom-in';
      img.addEventListener('click', () => window.open(img.src, '_blank'));
    });
  }
});
