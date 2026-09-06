# Cloud-Based-Password-Manager
# 🔐 Cloud-Based Password Manager

A simple and secure **Cloud-Based Password Manager** developed using HTML, CSS, JavaScript, Python Flask, SQLite, and encryption.

The application allows users to create an account, securely store their passwords, search saved credentials, edit or delete them, and generate strong passwords.

---

## 📌 Project Overview

Managing multiple passwords can be difficult and unsafe when passwords are stored in plain text or written down manually.

This project provides a simple web-based password vault where sensitive credentials are **encrypted before being stored in the database**.

### Main Flow

```text
User
  ↓
Frontend
  ↓
Flask Backend API
  ↓
Authentication
  ↓
Encryption / Decryption
  ↓
SQLite Database
```

---

## 🎯 Objectives

* Securely store user credentials
* Provide user authentication
* Encrypt stored passwords
* Allow users to add, view, edit and delete credentials
* Provide password search functionality
* Generate strong random passwords
* Demonstrate cloud-based application architecture

---

## 🏗️ System Architecture

```text
                 ┌──────────────────┐
                 │      USER        │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    FRONTEND      │
                 │ HTML/CSS/JS      │
                 └────────┬─────────┘
                          │
                     REST API
                          │
                          ▼
                 ┌──────────────────┐
                 │  FLASK BACKEND   │
                 │   Python API     │
                 └───────┬──────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       ┌──────────────┐      ┌──────────────┐
       │ Authentication│      │  Encryption  │
       └──────────────┘      └──────┬───────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │  SQLite Database│
                           └─────────────────┘
```

---

## ✨ Features

### 👤 User Registration

Users can create an account using:

* Name
* Email
* Master password

The master password is stored as a **password hash**, not as plain text.

### 🔑 User Login

Registered users can log into their personal password vault.

### 🔐 Password Encryption

Saved passwords are encrypted before being stored in the database.

```text
Original Password
       ↓
    Encryption
       ↓
Encrypted Password
       ↓
    Database
```

### 📂 Password Vault

Users can store:

* Website/service name
* Username/email
* Password
* Optional notes

### 🔎 Search

Users can search saved credentials by website or username.

### ✏️ Edit

Existing credentials can be updated.

### 🗑️ Delete

Users can remove credentials from their vault.

### 🎲 Password Generator

The application can generate strong random passwords containing:

* Uppercase letters
* Lowercase letters
* Numbers
* Special characters

---

## 🛠️ Technologies Used

| Technology   | Purpose                        |
| ------------ | ------------------------------ |
| HTML         | Frontend structure             |
| CSS          | User interface styling         |
| JavaScript   | Frontend interaction           |
| Python       | Backend programming            |
| Flask        | REST API framework             |
| SQLite       | Database                       |
| Cryptography | Password encryption            |
| Werkzeug     | Password hashing               |
| Flask-CORS   | Frontend-backend communication |
| GitHub       | Version control                |
| Render       | Cloud deployment               |

---

## 📁 Project Structure

```text
cloud-password-manager/
│
├── frontend/
│   ├── index.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   │
│   └── encryption/
│       └── crypto.py
│
├── database/
│   ├── schema.sql
│   └── README.md
│
├── .gitignore
└── README.md
```

---

# 🚀 How to Run the Project

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd cloud-password-manager
```

---

## 2. Install Python

Make sure Python 3.10 or later is installed.

Check:

```bash
python --version
```

---

## 3. Install Backend Dependencies

Open the terminal in the project folder:

```bash
pip install -r backend/requirements.txt
```

---

## 4. Initialize the Database

Create the SQLite database using the SQL schema:

```text
database/schema.sql
```

The database contains two main tables:

```text
users
vault
```

### Users Table

Stores:

* User ID
* Name
* Email
* Password hash

### Vault Table

Stores:

* Vault ID
* User ID
* Website
* Username
* Encrypted password
* Notes

---

## 5. Start the Backend

From the project root:

```bash
python backend/app.py
```

The Flask API will run at:

```text
http://127.0.0.1:5000
```

---

## 6. Start the Frontend

Open another terminal:

```bash
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

---

# 🔄 Application Workflow

```text
START
  ↓
Open Website
  ↓
Register / Login
  ↓
Authentication
  ↓
Password Vault
  ↓
Add Password
  ↓
Encrypt Password
  ↓
Store in Database
  ↓
Retrieve Credential
  ↓
Decrypt Password
  ↓
Display to Authenticated User
```

---

# 🔒 Security

The project uses different security mechanisms for different types of secrets.

### Master Password

The master password is **hashed** using Werkzeug before storage.

```text
Master Password
       ↓
Password Hashing
       ↓
Database
```

### Stored Credentials

Passwords saved inside the vault are **encrypted** using Fernet symmetric encryption.

```text
Password
   ↓
Fernet Encryption
   ↓
Encrypted Value
   ↓
Database
```

When an authenticated user requests a credential:

```text
Encrypted Value
       ↓
Decryption
       ↓
Original Password
```

---

# ☁️ Cloud Computing Concept

The application can be deployed to a cloud platform so that users can access it remotely.

```text
              INTERNET
                  │
                  ▼
        ┌──────────────────┐
        │ Cloud Deployment │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │  Flask Backend   │
        └────────┬─────────┘
                 │
        ┌────────▼─────────┐
        │ Cloud Database   │
        └──────────────────┘
```

Possible cloud deployment components include:

* Cloud-hosted Flask backend
* Cloud database
* Environment variables for secrets
* HTTPS
* Remote access

---

# 🌐 API Endpoints

| Method | Endpoint              | Purpose             |
| ------ | --------------------- | ------------------- |
| POST   | `/api/register`       | Register a user     |
| POST   | `/api/login`          | Authenticate user   |
| GET    | `/api/passwords`      | Get saved passwords |
| POST   | `/api/passwords`      | Add a password      |
| GET    | `/api/passwords/<id>` | Get one credential  |
| PUT    | `/api/passwords/<id>` | Update credential   |
| DELETE | `/api/passwords/<id>` | Delete credential   |

---

# 🧪 Example

A user saves:

```text
Website: GitHub
Username: student123
Password: MyStrongPassword@123
```

The database does **not** need to store the password as plain text.

Instead:

```text
MyStrongPassword@123
          ↓
      Encryption
          ↓
gAAAAA....encrypted-value....
```

When the authenticated user requests it, the backend decrypts it and returns the credential.

---

# 📊 Advantages

* Simple and user-friendly
* Centralized password management
* Password encryption
* User authentication
* Searchable password vault
* Strong password generation
* Can be accessed remotely after cloud deployment
* Demonstrates multiple cloud and security concepts

---

# ⚠️ Limitations

This project is designed as an **educational/college demonstration** and should not be treated as a production password manager.

A production system should additionally implement:

* HTTPS-only communication
* Secure cloud secret management
* Strong key-management architecture
* CSRF protection
* Rate limiting
* Secure session/token storage
* Multi-factor authentication
* Security auditing
* Database encryption and backups
* Extensive penetration/security testing

---

# 🔮 Future Enhancements

Possible future improvements include:

* 🔐 Two-factor authentication
* ☁️ Cloud-hosted database
* 📱 Mobile application
* 🌐 Browser extension
* 🔑 Password strength meter
* 📋 Secure clipboard copying
* 👥 Secure credential sharing
* 📜 Security audit logs
* 🔄 Automatic cloud backup
* 🛡️ Biometric authentication
* 🎨 Dark mode

---

# 🎓 Learning Outcomes

Through this project, we learn:

* Cloud application architecture
* REST API development
* Flask framework
* Frontend-backend communication
* Database management
* Authentication
* Password hashing
* Data encryption
* Git and GitHub
* Cloud deployment
* Basic cybersecurity principles

---

# 👨‍💻 Project Type

**Domain:** Cloud Computing + Cybersecurity

**Project:** Cloud-Based Password Manager

**Architecture:** Client – Server – Database

**Frontend:** HTML, CSS, JavaScript

**Backend:** Python Flask

**Database:** SQLite

**Encryption:** Fernet

---

## ⭐ Conclusion

The Cloud-Based Password Manager demonstrates how cloud application architecture and security techniques can be combined to create a centralized password-management system.

The project provides authentication, encrypted credential storage, password management, searching, editing, deletion, and password generation while demonstrating fundamental concepts of **cloud computing, web development, databases, and cybersecurity**.
