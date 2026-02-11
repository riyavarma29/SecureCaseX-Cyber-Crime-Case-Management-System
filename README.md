🔐 SecureCaseX – Cyber Crime Case Management System

SecureCaseX is a role-based Cyber Crime Case Management System designed to streamline digital investigation workflows. The platform enables administrators, investigators, and analysts to collaborate efficiently on cybercrime cases with structured case tracking, evidence management, and reporting capabilities.

🎯 Project Overview

SecureCaseX provides a secure and organized way to:

Create and manage cybercrime cases

Assign investigators and analysts

Track case status (Open, Investigating, Closed)

Manage digital evidence

Submit analytical reports

Generate system statistics and reports

The system ensures role-based access control and prevents unauthorized actions.

👥 User Roles
👨‍💼 Admin

Manage users and roles

Create cases

Assign investigators and analysts

Monitor system-wide statistics

View reports

🕵️ Investigator

View assigned cases

Upload and manage evidence

Update case status

Track investigation progress

🔎 Analyst

View assigned cases

Analyze case evidence

Submit analysis reports

Recommend case status updates

🧩 Core Features

✅ Role-Based Authentication System

✅ Secure Login & Signup

✅ Case Creation & Assignment

✅ Evidence Tracking

✅ Case Status Workflow (Open → Investigating → Closed)

✅ Analyst Report Submission

✅ Case Statistics Dashboard

✅ Prevention of Multiple Admin Accounts

✅ Status Validation Logic

✅ Django ORM Based Filtering & Aggregation

✅ Clean Dashboard UI

📊 Case Workflow

Admin creates a case (default: Open)

Admin assigns Investigator → Status becomes Investigating

Investigator uploads evidence & updates progress

Admin assigns Analyst

Analyst submits analysis report

Case marked as Closed

🛠️ Tech Stack

Backend: Django (Python)

Database: SQLite (can be extended to PostgreSQL)

Frontend: HTML, CSS, Bootstrap

Authentication: Django Authentication System

ORM: Django ORM with QuerySet filtering & aggregation

🧠 Technical Highlights

Used Django decorators for role-based access control

Implemented custom user model with role field

Optimized queries using annotate() and Count()

Used Django messages framework for user feedback

Prevented invalid case status transitions

Enforced single admin registration logic

Applied secure permission checks in views

📈 System Reports

Total Cases

Open Cases

Investigating Cases

Closed Cases

Active / Inactive Users

🔒 Security Measures

Login required for all dashboards

Role-based view restrictions

Prevention of unauthorized role modification

Status validation before saving

Protection against deleting self-account
