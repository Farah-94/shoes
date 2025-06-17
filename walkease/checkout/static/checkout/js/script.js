// Ensure you load Stripe.js in your HTML, then use this file

// Replace the template variable with your actual publishable key passed from your Django view.
const stripePublicKey = window.stripePublicKey; // This global variable should be set in the template.
const stripe = Stripe(stripePublicKey);

// Function to create a PaymentIntent by calling your backend view
async function createPaymentIntent() {
  try {
    // Make a request to your backend to create a PaymentIntent
    const response = await fetch('/checkout/create-payment-intent/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    return data.client_secret;
  } catch (error) {
    console.error("Error creating PaymentIntent:", error);
  }
}

// Call the function and initialize Stripe Elements
createPaymentIntent().then(clientSecret => {
  if (!clientSecret) {
    console.error("No client secret returned!");
    return;
  }
  
  // Create an instance of Elements and mount the card Element
  const elements = stripe.elements();
  const cardElement = elements.create('card');
  cardElement.mount('#payment-element');
  
  // When the form is submitted, confirm the payment
  const form = document.getElementById('payment-form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();
    stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: cardElement,
      }
    }).then(function(result) {
      if (result.error) {
        // Display error in your UI
        document.getElementById('payment-message').textContent = result.error.message;
      } else {
        if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
          // Payment was successful
          window.location.href = "/order-success/";  // Change this URL to your actual order success path
        }
      }
    });
  });
});