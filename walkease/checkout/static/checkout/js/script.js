// static/checkout/js/script.js

// 0) Initialize Stripe with your publishable key
const stripe     = Stripe(window.stripePublicKey);
const intentUrl  = window.paymentIntentUrl;
const successUrl = window.paymentSuccessUrl;  // now already "https://…/checkout/success/"

// 1) CSRF helper for Django
function getCookie(name) {
  let value = null;
  document.cookie.split(";").forEach(cookie => {
    const [k, v] = cookie.trim().split("=");
    if (k === name) value = decodeURIComponent(v);
  });
  return value;
}
const csrftoken = getCookie("csrftoken");

// 2) Fetch a client_secret from your backend
async function createPaymentIntent() {
  const resp = await fetch(intentUrl, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    }
  });
  if (!resp.ok) {
    throw new Error(`PaymentIntent error: ${await resp.text()}`);
  }
  const { client_secret: clientSecret } = await resp.json();
  return clientSecret;
}

// 3) Main flow
document.addEventListener("DOMContentLoaded", async () => {
  console.log("🚀 Initializing payment flow…");

  let clientSecret;
  try {
    clientSecret = await createPaymentIntent();
    console.log("🔒 clientSecret:", clientSecret);
  } catch (err) {
    console.error(err);
    document.getElementById("payment-message").textContent = err.message;
    return;
  }

  // 4) Set up Stripe Elements
  const elements = stripe.elements({ clientSecret });
  const paymentEl = elements.create("payment");
  paymentEl.mount("#payment-element");

  // 5) Handle form submission
  const form = document.getElementById("payment-form");
  form.addEventListener("submit", async e => {
    e.preventDefault();
    document.getElementById("submit").disabled = true;

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: { return_url: successUrl }
    });

    if (error) {
      console.error("Payment failed:", error);
      document.getElementById("payment-message").textContent = error.message;
      document.getElementById("submit").disabled = false;
    }
    // On success, Stripe.js will auto-redirect to successUrl
  });
});
