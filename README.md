# Fitness Class Booking API (Django REST Framework)

This is a backend-only Django REST API for managing fitness classes and bookings with timezone support.

## 🚀 Features

- Create and list fitness classes (with date and time)
- Book multiple slots in a class (until available slots are exhausted)
- List bookings by email
- Timezone-aware scheduling (default: IST)
- Delete fitness classes
- Class name uniqueness and slot validation
- Basic test cases included

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AMANKUMAR22MCA/booking-api-django.git
cd booking-api-django
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Run Development Server

```bash
python manage.py runserver
```

### 6. Run Tests

```bash
python manage.py test
```

## 📦 API Endpoints

| Method | Endpoint       | Description |
|--------|----------------|-------------|
| GET    | `/classes/`    | List upcoming fitness classes |
| POST   | `/classes/`    | Create a new fitness class |
| DELETE | `/classes/<class_id>/delete/` | Delete a class by ID |
| POST   | `/book/`       | Book slots in a class |
| GET    | `/bookings/?email=user@example.com&tz=Asia/Kolkata` | View bookings by email (with timezone) |

## ⏱ Timezone Support

Add `tz=<timezone>` in the bookings API (e.g., `America/New_York`, `Asia/Kolkata`).

