// static/checkout/js/script.js

// 0) Initialize Stripe with the publishable key your template injected
const stripe     = Stripe(window.stripePublicKey);
const intentUrl  = window.paymentIntentUrl;
const successUrl = window.paymentSuccessUrl;

// 1) Helper to read Django’s CSRF token from cookies
function getCookie(name) {
  let cookieValue = null;
  document.cookie.split(';').forEach(c => {
    const [k, v] = c.trim().split('=');
    if (k === name) cookieValue = decodeURIComponent(v);
  });
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// 2) Ask your backend to create a PaymentIntent
async function createPaymentIntent() {
  const resp = await fetch(intentUrl, {
    method: 'POST',
    credentials: 'same-origin',   // send cookies, including CSRF
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  });
  if (!resp.ok) {
    throw new Error(`PaymentIntent error: ${await resp.text()}`);
  }
  const { client_secret: clientSecret } = await resp.json();
  return clientSecret;
}

// 3) Main entry point: run after the DOM is ready
document.addEventListener("DOMContentLoaded", async () => {
  let clientSecret;
  try {
    clientSecret = await createPaymentIntent();
  } catch (err) {
    console.error(err);
    document.getElementById('payment-message').textContent = err.message;
    return;
  }

  // 4) Initialize Stripe Elements with the client secret
  const elements = stripe.elements({ clientSecret });

  // 5) Mount the all-in-one Payment Element
  const paymentElement = elements.create('payment');
  paymentElement.mount('#payment-element');

  // 6) Handle your form submission
  const form = document.getElementById('payment-form');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    document.getElementById('submit').disabled = true;

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: successUrl
      }
    });

    if (error) {
      document.getElementById('payment-message').textContent = error.message;
      document.getElementById('submit').disabled = false;
    }
    // On success, Stripe.js automatically redirects to return_url
  });
});
