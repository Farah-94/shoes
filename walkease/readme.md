    # Walkease

## Table of Contents
- [Introduction](#introduction)
- [Purpose](#purpose)
- [Deployment](#deployment)
- [User Experience](#user-experience)
- [Design](#design)
- [Colour Scheme](#colour-scheme)
- [Typography](#typography)
- [Imagery](#imagery)
- [Testing](#testing)
- [Programme Used](#programme-used)

---

## Introduction
Walkease is an online boutique dedicated to women’s footwear, offering a curated selection of styles—from elegant heels and chic flats to sporty sneakers and cozy boots. Browse our diverse collection, pick your favorite designs, and choose from a full range of sizes to find the perfect fit. When you’re ready to check out, our seamless Stripe-powered payment flow delivers a real-life, secure checkout experience in just a few clicks. Whether you’re dressing up for a night out or keeping it casual for your daily routine, Walkease makes shopping for women’s shoes effortless and enjoyable. 

This project is organized into four Django apps—store, cart, checkout, and user—each responsible for a core piece of functionality and paired with its own templates and views:

**store Powers the public storefront:**

- Home page with featured collections
- Product listing and filtering
- Product detail pages (images, descriptions, reviews)

**cart Manages the shopping cart lifecycle:**

- Add or remove items
- Adjust quantities 
- View a real-time cart summary before checkout

**checkout Handles secure payments and order finalization:**

- Creates Stripe PaymentIntents on the backend
- Renders a PCI-compliant Stripe Elements form
- Redirects to an “Order Success” page once payment completes

**user Stores and displays customer profiles:**

- View and edit personal details (name, address, avatar)
- Review order history
- Admin-specific dashboard for superusers

By dividing responsibilities across these four apps, Walkease delivers a clean, maintainable full-stack site that’s easy to extend—whether you’re adding new product categories, swapping payment gateways, or enhancing user profiles.

  

## Purpose
The goal of Walkease is to deliver a polished, user-friendly online store that showcases products with clear imagery, intuitive navigation, and a streamlined purchase process. It’s designed for small retailers who want a turnkey solution with Django’s robustness and Stripe’s reliability.

## Deployment
How to Run the Project Locally
**Github**
A Github account. Create a Github Account [here](https://github.com join)
Use the Chrome browser then follow these steps:
Install the Gitpod Browser Extension for Chrome
After installation, restart the browser
Log into Gitpod with your Gitpod account
Navigate to the Project Github repository
Click the green "Gitpod" button in the top right corner of the repository
This will trigger a new Gitpod workspace to be created from the code in Github where you can work locally.
To work on the project code within a local IBE such as VSCode, Pycharm, etc.
Follow the link to the Project Repository
Under the repository name, click "clone or download".
In the clone with HTTPs section, copy the clone URL for the repository
In your local IBE, open the terminal
Change the current working directory to the location where you want the cloned directory to be made.
Type git clone, and then paste the URL you copied in Step 3: https://github.com/Farah-94/shoes.git
Press Enter. Your local clone will be created.

**Heroku Deployment**
Login to Heroku.
In your Heroku dashboard, click "New" and then "Create new app".
Provide a unique name for your app (e.g., walkease) and choose your region.
Go to the "Resources" tab within your Heroku app.
Under Dynos, select the appropriate plan. Heroku’s Eco Dynos help you stay within a low-cost, sustainable usage model.
Connect your app to Github
Navigate to the "Deploy" tab in your Heroku app dashboard.
If prompted, connect your GitHub account.
Write in the search "shoes".
Once found, click "Connect" to link your repository.
After linking, scroll down in the Deploy section.
Click on the automatic deploy( automatic update after pushing code to github).
Click "Deploy Branch" to manually deploy your current branch.
Review the build logs to ensure that the deployment completes successfully.
https://git.heroku.com/walkease-app.git git url created.

## User Experience
### First-time Visitor

- For first-time visitors, we aim to make your initial interaction smooth and intuitive.
- The website is designed with a straightforward layout, making it easy to explore and easy to understand.
- Users can find their expected results without any hassel.
- Users can access product page in Menu, then select products.
- Users can see product details by clicking the product card.
- Users will be able to select sizes ranging from 6-9, set the quanty and add the product in cart.
- Users can adjust quantities or remove items as needed, ensuring a flexible and user-friendly shopping experience.
- Users can proceeds and go to the checkout, where they need to fill out shiiping and payment form.
- Users can see the order successfull screen message with two options continue shopping and profile after completing order.

### Return Visitor

- For return visitors, we focus on advertising products in more efficient ways.
- Stay informed with the latest products and special discount offers.

### Visitor Goals

- Enable users to add products to their cart, update quantities, and remove items seamlessly, ensuring that managing their selections is both straightforward and efficient.
- Provide a secure, simple checkout process to build trust and ensure that every completed purchase is effortless.
- For frequent visitors, the site highlights the latest products and exclusive discount offers, ensuring that they stay informed and enjoy a tailored shopping experience.
- Simplify account creation and sign-in processes so that visitors can easily register, log in, and track their orders, further enhancing their engagement with our platform.

## Design
Walkease features a minimal, clean aesthetic:
- Generous whitespace to let product imagery shine.
- Consistent button styles and form inputs.
- Clear hierarchy using headings, subheadings, and highlighted call-to-action elements.

**Wireframes**

## Colour Scheme
- **Primary:** #2C3E50 (Charcoal Blue)
- **Accent:** #27AE60 (Vibrant Green) for buttons and links
- **Background:** #F8F9FA (Light Grey) for page backgrounds
- **Text:** #333333 (Dark Grey) for body copy

## Typography
- **Headings:** “Lora”, serif, for a touch of elegance
- **Body Copy:** “Roboto”, sans-serif, for readability
- **Fallbacks:** system fonts such as Arial, Helvetica

## Imagery
- High-resolution product photos with consistent aspect ratios.
- On-page banners showcasing new arrivals or promotions.
- Placeholder graphics sourced from Unsplash and customized with brand colors.

## Testing


- **Manual QA:** Stripe test cards (e.g., 4242 4242 4242 4242 for success, 4000 0000 0000 9995 for insufficient funds).


## Programme Used
-  Django 5.2.1, Python 3.12
-  HTML5, CSS3, JavaScript (ES6+)
-  Stripe.js v3, Stripe Python SDK
-  Heroku, WhiteNoise
-  Git, GitHub
-  PostgreSQL (via Heroku Postgres)
-  Freepiks
-  Formspree
-  Logo maker

