eCommerce API
Project Overview
This is a RESTful API for an eCommerce platform, built with Django and Django REST Framework. The API allows users to perform various operations such as browsing products, managing carts, placing orders, and making payments via Paystack. It also includes functionality for user authentication, profile management, and order tracking.

Features
User Authentication: Secure user registration and login.
Product Management: View, create, update, and delete products (Admin only).
Category Management: Manage product categories.
Cart System: Add/remove items from the cart and view the cart's total.
Checkout Process: Users can place orders and make payments.
Shipping and Orders: Manage shipping addresses and track order statuses.
Payment Integration: Integrated with Paystack for seamless payments.
User Profiles: Authenticated users can create and manage their profiles.
Technologies Used
Backend: Django, Django REST Framework
Database: SQLite (for development) / PostgreSQL (for production)
Payment Integration: Paystack API
Authentication: JWT (JSON Web Token)
Getting Started
Prerequisites
Make sure you have the following installed:

Python 3.x
Django
Django REST Framework
PostgreSQL (for production)
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/ecommerce-api.git
Navigate to the project directory:

bash
Copy code
cd ecommerce-api
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the environment variables: Create a .env file and add the following:

bash
Copy code
SECRET_KEY=your_secret_key
DEBUG=True
PAYSTACK_SECRET_KEY=your_paystack_key
Run migrations:

bash
Copy code
python manage.py migrate
Start the server:

bash
Copy code
python manage.py runserver
Running Tests
To run the tests, use:

bash
Copy code
python manage.py test
API Endpoints
Here are the primary API endpoints:


Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.