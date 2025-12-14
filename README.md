Project Overview:

This project is a Mini Instagram Clone built using Python (Flask) for the backend, HTML & CSS for the frontend, and MySQL as the database.
The application replicates core Instagram features such as user authentication, post creation, likes, comments, and feed display.
The goal of this project is to demonstrate backend logic, database relationships, authentication handling, and full-stack integration using a simple and beginner-friendly tech stack.

Features Implemented:
 
User Authentication:

User Signup with username, email, and password
User Login with password hashing using Werkzeug
Session-based authentication
Secure logout functionality

Post Management:

Authenticated users can create posts
Each post contains:
Image URL
Caption
Posts are stored in the MySQL database

Feed System:

Displays all posts in reverse chronological order
Shows:
Username
Post image
Caption
Feed is dynamically rendered using Flask templates
Likes System
Logged-in users can like posts


Comments System:

Users can comment on posts
Comments are linked to both users and posts

Access Control:

Only authenticated users can:
Create posts
Like or comment on posts
View the feed
Unauthorized users are redirected to the login page

Technology Stack:

| Layer              | Technology                |
| ------------------ | ------------------------- |
| Backend            | Python, Flask             |
| Frontend           | HTML, CSS                 |
| Database           | MySQL                     |
| Authentication     | Werkzeug Password Hashing |
| Session Management | Flask Sessions            |

Database Design:

The project uses relational database design with the following tables:

users – Stores user credentials
posts – Stores post data
likes – Manages post likes (many-to-many)
comments – Stores user comments on posts
followers – (Optional extension for follow system)

This structure demonstrates one-to-many and many-to-many relationships.

Project Structure:

instagramclone
│
├── app.py
├── db.py
├── requirements.txt
│
├── templates
│   ├── login.html
│   ├── signup.html
│   ├── feed.html
│   ├── createpost.html
│
└── static
    └── style.css


How to Run the Project:

1️) Install Dependencies
pip install flask mysql-connector-python werkzeug

2️) Start MySQL and Create Database
CREATE DATABASE instagramclone;
(Create tables as per schema)

3) Run the Application
python app.py

4) Open in Browser
http://127.0.0.1:5000

Learning Outcomes:

Understanding Flask routing and request handling
Implementing secure user authentication
Working with MySQL and relational data
Handling CRUD operations
Debugging real backend issues
Building a full-stack web application
Future Enhancements



Profile pages:

Display likes & comment count
Image upload using Cloudinary or local storage
API version using JWT authentication
Frontend enhancement using React

Conclusion:

This project showcases a working Instagram-style application with clean backend logic and database integration.
It is ideal for learning Flask, backend development, and full-stack fundamentals, and suitable for academic submission or internship evaluation.
