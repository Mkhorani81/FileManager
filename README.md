# 📁 File Manager

A **Django REST API** project for managing user files and authentication.  
This project uses **Django REST Framework (DRF)**, **PostgreSQL**, **JWT Authentication**, and **Docker** for containerization.

---

## 🧠 Overview

The **File Manager** API allows users to manage files securely and authenticate using a **custom login with phone number and password**.  
It supports API testing via **Postman** and automated testing using **Django’s built-in test framework**.

---

## 🧩 Tech Stack

| Technology | Purpose |
|-------------|----------|
| **Python 3.12+** | Backend language |
| **Django** | Core web framework |
| **Django REST Framework (DRF)** | RESTful API support |
| **PostgreSQL** | Database |
| **JWT (JSON Web Token)** | Authentication |
| **Docker & Docker Compose** | Containerization |
| **Postman** | API testing |
| **Django Test Framework** | Unit and integration tests |

---

## ⚙️ Setup and Installation

### 1️⃣ Clone the Repository
```bash
after cloning from git
cd FileManager
```

### 2️⃣ Environment Variables

Create a `.env` file in the **root directory** (same level as `manage.py`) and configure it like this:

```env
SECRET_KEY = ******
DEBUG = False
ALLOWED_HOSTS=localhost,127.0.0.1,web
FILES_ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png,zip,txt
MAX_FILE_SIZE_MB=100



# Database
ENGINE = postgresql
POSTGRES_DB = filemanager_db
POSTGRES_USER = *******
POSTGRES_PASSWORD = ******
DB_HOST= db
DB_PORT= 5432
```

---

### 3️⃣ Run with Docker

To build and start the containers:
```bash
docker-compose up -d --build
```

After successful build, open your browser at:
```
http://127.0.0.1
```
or  
```
http://localhost
```

The project runs by default on **port 80**.

---

## 👤 Superuser Creation

After the container is up, run the following inside the Django container:
```bash
python manage.py createsuperuser
```

You will be prompted for:
- **Phone number**
- **Password**

This project uses **custom authentication** with `phone_number` and `password`.

---

## 🧪 Running Tests

To execute automated tests:
```bash
python manage.py test
```

Tests are written using:
- `using python uniitest`
- `Test Case in Django and DRF`

---

## 🧭 API Testing with Postman

You can test all API endpoints using **Postman**.  
Put postman collection in root directory too

---

## 🐳 Docker Services

| Service | Description |
|----------|-------------|
| **app** | Django + Gunicorn application |
| **db** | PostgreSQL database |
| **nginx** | Reverse proxy for static/media files |

-

---
