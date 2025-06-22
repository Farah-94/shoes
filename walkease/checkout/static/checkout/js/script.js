// static/checkout/js/script.js

// grab keys & URLs the template set
const stripe    = Stripe(window.stripePublicKey);
const intentUrl = window.paymentIntentUrl;
const successUrl = window.paymentSuccessUrl;

// helper to read the CSRF token cookie
function getCookie(name) {
  let cookieValue = null;
  document.cookie.split(';').forEach(c => {
    const [k,v] = c.trim().split('=');
    if (k === name) cookieValue = decodeURIComponent(v);
  });
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

async function createPaymentIntent() {
  const resp = await fetch(intentUrl, {
    method: 'POST',
    credentials: 'same-origin',         // send cookies
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken         // Django’s CSRF header
    }
  });
  if (!resp.ok) throw new Error(await resp.text());
  const data = await resp.json();
  return data.client_secret;
}

document.addEventListener("DOMContentLoaded", async () => {
  let clientSecret;
  try {
    clientSecret = await createPaymentIntent();
  } catch (err) {
    console.error("PaymentIntent error:", err);
    document.getElementById('payment-message').textContent = err.message;
    return;
  }

  // mount Stripe’s Card Element
  const elements = stripe.elements();
  const card = elements.create('card');
  card.mount('#payment-element');

  // handle the form
  document.getElementById('payment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    document.getElementById('submit').disabled = true;

    const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
      payment_method: { card }
    });

    if (error) {
      document.getElementById('payment-message').textContent = error.message;
      document.getElementById('submit').disabled = false;
    } else if (paymentIntent && paymentIntent.status === 'succeeded') {
      window.location.href = successUrl;
    }
  });
});
