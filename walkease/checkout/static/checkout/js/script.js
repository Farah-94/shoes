// static/checkout/js/script.js

// Grab the Stripe key and URLs injected by your template
const stripe       = Stripe(window.stripePublicKey);
const intentUrl    = window.paymentIntentUrl;
const successUrl   = window.paymentSuccessUrl;

// Helper to read Django’s CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  document.cookie.split(';').forEach(c => {
    const [k, v] = c.trim().split('=');
    if (k === name) cookieValue = decodeURIComponent(v);
  });
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Call your backend to create a PaymentIntent and return its client_secret
async function createPaymentIntent() {
  const resp = await fetch(intentUrl, {
    method: 'POST',
    credentials: 'same-origin',      // ensures cookies (including CSRF) are sent
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  });
  if (!resp.ok) {
    throw new Error(`PaymentIntent error: ${await resp.text()}`);
  }
  const data = await resp.json();
  return data.client_secret;
}

// Main entry point
document.addEventListener("DOMContentLoaded", async () => {
  let clientSecret;
  try {
    clientSecret = await createPaymentIntent();
  } catch (err) {
    console.error(err);
    document.getElementById('payment-message').textContent = err.message;
    return;
  }

  // 1) Initialize Stripe Elements with the client secret
  const elements = stripe.elements({ clientSecret });

  // 2) Mount the Payment Element into your form
  const paymentElement = elements.create('payment');
  paymentElement.mount('#payment-element');

  // 3) Handle form submission
  const form = document.getElementById('payment-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    document.getElementById('submit').disabled = true;

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        // Stripe will redirect here on successful payment
        return_url: successUrl
      }
    });

    if (error) {
      document.getElementById('payment-message').textContent = error.message;
      document.getElementById('submit').disabled = false;
    }
    // On success, Stripe auto-redirects to successUrl
  });
});
