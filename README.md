Name:- Srishti Sharma

Project title :- Course Registration Form

Description of the Project :-

🧾 Project Overview

This is a web-based Course Registration System that allows students to:

Create an account

Log in

View available courses

Register for courses

See a list of registered courses

The project is built using:

Python 3

Flask (Backend Web Framework)

SQLite (Database)

HTML/CSS (Frontend Templates)

🛠 Features

👨‍🎓 Student Module

Student registration

Student login/logout

Browse all available courses

Register for courses

View personal course registrations

🗄 Database Operations

Store students

Store courses

Map enrolled students to courses

Prevent duplicate registrations

📦 Tech Stack

Component Technology

Backend Python + Flask

Database SQLite

Frontend HTML + CSS (Jinja2 templates)

Server Localhost (Flask built-in)

📁 Folder Structure

course-registration-system/

│── app.py # Main Flask application

│── db.py # Database connection helper

│── schema.sql # Tables & sample seed data

│── requirements.txt # Python dependencies

│── README.md

│

├── templates/ # HTML UI pages

│ ├── base.html

│ ├── index.html

│ ├── login.html

│ ├── register.html

│ ├── dashboard.html

│ ├── courses.html

│ └── my_courses.html

│ └── static/

└── styles.css    # UI styling

👩‍💻 Usage Flow
Register
Click Register

Enter name, email, password

Login
Enter registered email + password

Dashboard
Navigate using navigation bar

Register for Courses
Click Courses

Press Register button on a course

View My Courses
Click My Courses

Shows all registered courses

🗄 Database Schema

students

Column Type

id INTEGER PRIMARY KEY

name TEXT

email TEXT UNIQUE

password TEXT

courses

Column Type

id INTEGER PRIMARY KEY

code TEXT UNIQUE

title TEXT

credits INTEGER

enrollments

Column Type

id INTEGER PRIMARY KEY

student_id INTEGER

course_id INTEGER

UNIQUE(student_id, course_id)
