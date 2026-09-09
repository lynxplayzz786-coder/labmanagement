# 🔬 BCA_29 — Lab Equipment Rental & Management System

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2_LTS-green)](https://djangoproject.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)](https://mysql.com)

> **Project Code:** BCA_29  
> **College:** [Your College Name]  
> **Supervisor:** Ms. Manisha Chawla  
> **Academic Year:** 2024-25  

---

## 📋 Project Overview

A web-based system to automate lab equipment rental across college computer labs.
Replaces manual registers with a role-based digital platform supporting:
- Equipment inventory management with QR codes
- Booking lifecycle: Request → Approve → Issue → Return
- Maintenance tracking with automatic stock control
- Real-time analytics dashboard with Chart.js

---

## 👥 User Roles

| Role | What they can do |
|------|-----------------|
| **Admin** | Full access — equipment CRUD, approve/reject, reports, maintenance |
| **Staff** | Approve requests, issue/return equipment, maintenance |
| **Faculty** | Browse equipment, request bookings, view own history |
| **Student** | Browse equipment, request bookings, view own history |

---

## 🚀 Quick Setup

### Prerequisites
- Python 3.11+
- MySQL 8.0 running on port 3306

### 1. Clone & Navigate
```bash
cd LabManagement
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
Make sure MySQL is running. The project uses:
- **Host:** localhost:3306
- **DB Name:** lab_management_db
- **User:** root
- **Password:** abhishek123

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Load Sample Data
```bash
python seed_data.py
```
This creates:
- 7 equipment categories
- 5 labs (Lab A → Lab E)
- 10 equipment items with auto-generated QR codes
- 4 demo users (admin, staff1, faculty1, student1)

### 7. Start the Server
```bash
python manage.py runserver
```

**Open:** http://127.0.0.1:8000

---

## 🔑 Demo Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `abhishek123` |
| Staff | `staff1` | `staff123` |
| Faculty | `faculty1` | `faculty123` |
| Student | `student1` | `student123` |

---

## 📁 Project Structure

```
LabManagement/
├── lab_management/        # Django project config
│   ├── settings.py
│   └── urls.py
├── accounts/              # Auth + User roles
│   ├── models.py          # CustomUser (role field)
│   ├── views.py           # Login, Register, Profile
│   ├── forms.py           # Auth + Profile forms
│   └── decorators.py      # @role_required
├── equipment/             # Equipment module
│   ├── models.py          # Equipment, Category, Lab
│   ├── views.py           # CRUD + QR display
│   └── forms.py           # EquipmentForm + Filter
├── bookings/              # Booking lifecycle
│   ├── models.py          # Booking, IssueLog, Maintenance
│   ├── views.py           # Full booking workflow
│   └── forms.py           # BookingForm, ReturnForm
├── dashboard/             # Analytics
│   ├── views.py           # Role-based dashboards + Charts
├── templates/             # All HTML templates
│   ├── base.html          # Master layout
│   ├── accounts/          # login, register, profile
│   ├── equipment/         # list, detail, add_edit, qr
│   ├── bookings/          # booking, manage, return, maintenance
│   └── dashboard/         # admin, staff, student, reports
├── static/css/style.css   # Complete design system
├── seed_data.py           # Demo data loader
└── requirements.txt
```

---

## ⚙️ Business Rules Implemented

1. **BR-1:** Staff must verify availability before approving
2. **BR-2:** Booking quantity cannot exceed available stock
3. **BR-3:** Return date must be after booking start date
4. **BR-4:** Final availability check before physical issue
5. **BR-5:** Good condition return → stock automatically restored
6. **BR-6:** Damaged/Lost → maintenance record created, stock NOT restored
7. **BR-7:** Maintenance resolve → stock restored automatically
8. **BR-8:** Overdue tracking — due date highlighted in red
9. **BR-9:** Admin cannot delete equipment with active bookings

---

## 📦 Key Dependencies

```
Django==4.2.16
mysqlclient==2.2.4
django-crispy-forms==2.3
crispy-bootstrap5==2024.2
Pillow==10.4.0
qrcode==8.0
```

---

## 📊 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + Django 4.2 LTS |
| Database | MySQL 8.0 |
| Frontend | HTML5 + CSS3 + Bootstrap 5.3 |
| Charts | Chart.js 4.4 |
| Icons | Font Awesome 6.5 |
| QR Code | qrcode (Python library) |
| Fonts | Google Fonts (Poppins) |

---

## 🧪 Testing

Test the complete booking lifecycle:
1. Login as **student1** → Browse Equipment → Book Arduino Uno
2. Login as **staff1** → Manage Bookings → Approve → Issue
3. Login as **staff1** → Return (mark as Damaged)
4. Login as **staff1** → Maintenance → Resolve
5. Check stock restored in Equipment detail

---

*Submitted to Ms. Manisha Chawla | BCA Department | BCA_29*
