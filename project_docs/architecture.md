# 🏗️ Architecture

## System Architecture Overview

```
                USER (Browser)
                     │
                     ↓
           ┌─────────────────────┐
           │      Frontend       │
           │   HTML / CSS / JS   │
           │     Bootstrap 5     │
           │      Chart.js       │
           └──────────┬──────────┘
                      │  HTTP Request/Response (Django Templates)
                      ↓
           ┌─────────────────────┐
           │   Django Backend    │
           │                     │
           │  urls.py → views.py │
           │  forms.py           │
           │  models.py (ORM)    │
           │  Business Logic     │
           └──────────┬──────────┘
                      │  Django ORM
                      ↓
           ┌─────────────────────┐
           │        MySQL        │
           │  lab_management DB  │
           └─────────────────────┘
```

---

## Django Project & App Structure

```
lab_management/                    ← Django Project Root
│
├── lab_management/                ← Project Config
│   ├── settings.py                (DB, installed apps, static, media)
│   ├── urls.py                    (Root URL dispatcher)
│   └── wsgi.py
│
├── accounts/                      ← Auth + User Roles
│   ├── models.py                  (CustomUser with role field)
│   ├── views.py                   (Login, Register, Logout, Profile)
│   ├── forms.py                   (LoginForm, RegisterForm)
│   ├── urls.py
│   ├── decorators.py              (role_required decorator)
│   └── templates/accounts/
│       ├── login.html
│       └── register.html
│
├── equipment/                     ← Equipment + Category + Lab + Inventory
│   ├── models.py                  (Equipment, Category, Lab)
│   ├── views.py                   (CRUD, Search, Filter, QR generation)
│   ├── forms.py                   (EquipmentForm, CategoryForm)
│   ├── urls.py
│   ├── utils.py                   (QR code generator, asset_id generator)
│   └── templates/equipment/
│       ├── list.html
│       ├── detail.html
│       ├── add_edit.html
│       └── qr.html
│
├── bookings/                      ← Booking Lifecycle
│   ├── models.py                  (Booking, IssueLog)
│   ├── views.py                   (Request, Approve, Reject, Issue, Return)
│   ├── forms.py                   (BookingForm, ReturnForm)
│   ├── urls.py
│   └── templates/bookings/
│       ├── my_bookings.html       (Student/Faculty view)
│       ├── manage_bookings.html   (Staff/Admin view)
│       ├── booking_form.html
│       └── return_form.html
│
├── dashboard/                     ← Role-based Dashboards + Reports
│   ├── views.py                   (Stats, Charts data API, Reports)
│   ├── urls.py
│   └── templates/dashboard/
│       ├── admin_dashboard.html
│       ├── staff_dashboard.html
│       └── student_dashboard.html
│
├── templates/                     ← Global Templates
│   └── base.html                  (Navbar, Sidebar, Footer, JS/CSS includes)
│
├── static/                        ← CSS, JS, Images
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
│
├── media/                         ← Uploaded files (equipment photos, QR)
│
├── manage.py
└── requirements.txt
```

> ⚠️ **Note:** No separate `inventory` app. Equipment quantities (`quantity`, `available_quantity`) are managed inside the `equipment` app itself. Keeping it simple.

---

## User Role Architecture

```
         ┌─────────────────────────────────────┐
         │                SYSTEM               │
         └─────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ↓                 ↓                 ↓                ↓
       ADMIN           LAB STAFF          FACULTY          STUDENT
         │                 │                 │                │
   All permissions    Manage Issues     Request Booking   Request Booking
   User Management    Approve/Reject    View own history  View own history
   Equipment CRUD     Issue/Return      View equipment    View equipment
   Reports            Condition check   (cannot approve)  (cannot approve)
   Dashboard (full)   Dashboard         Dashboard         Dashboard
   Category/Lab CRUD
```

---

## Booking Workflow — State Machine

```
                  STUDENT / FACULTY
                        │
                        ↓ submit
              ┌──────────────────┐
              │   PENDING        │  booking_ref = BK-{year}-{seq}
              └────────┬─────────┘  auto-generated on save
                       │
            STAFF / ADMIN reviews
              ┌────────┴────────┐
            REJECT           APPROVE
              │                 │
              ↓                 ↓
           REJECTED          APPROVED
                                │
                    STAFF issues equipment
                                │
                                ↓
                            ISSUED
                    (available_quantity -= booked_qty)
                                │
                    STUDENT / FACULTY returns
                                │
                                ↓
                    Staff checks condition
              ┌─────────────────┴──────────────────┐
            GOOD                               DAMAGED / LOST
              │                                     │
              ↓                                     ↓
          COMPLETED                          MAINTENANCE REQUIRED
   available_quantity += qty            available_quantity NOT restored
                                        until Maintenance resolved
```

---

## URL Routing Plan

```
/                            → Redirect to login or dashboard
/login/                      → Login
/register/                   → Register
/logout/                     → Logout

/dashboard/                  → Role-based dashboard redirect

/equipment/                  → Equipment list (all roles)
/equipment/add/              → Add equipment (admin only)
/equipment/<id>/             → Equipment detail
/equipment/<id>/edit/        → Edit equipment (admin only)
/equipment/<id>/delete/      → Delete equipment (admin only)
/equipment/<id>/qr/          → View/download QR code

/bookings/                   → My bookings (student/faculty)
/bookings/new/               → New booking request
/bookings/<id>/              → Booking detail
/bookings/manage/            → Manage all bookings (staff/admin)
/bookings/<id>/approve/      → Approve booking
/bookings/<id>/reject/       → Reject booking
/bookings/<id>/issue/        → Issue equipment
/bookings/<id>/return/       → Process return

/reports/                    → Reports page (admin)
/reports/equipment-usage/    → Equipment usage report
/reports/maintenance/        → Maintenance report

/admin/                      → Django built-in admin panel
```

---

## Data Flow — Example: Student Books Arduino

```
1. Student logs in → role='student' → redirect to student_dashboard
2. Student goes to /equipment/ → sees Arduino Uno (Available: 15)
3. Student clicks "Book" → /bookings/new/?equipment=LAB-ARD-001
4. Student fills form: Quantity=2, Date: 15 Aug
5. Form submits → Booking created → status=PENDING, ref=BK-2026-001
6. Staff sees new pending request in manage_bookings
7. Staff clicks Approve → status=APPROVED
8. Staff clicks Issue → status=ISSUED, available_quantity: 15→13
9. Student returns on 16 Aug → Staff opens return form
10. Staff marks condition=GOOD → status=COMPLETED, available_quantity: 13→15
```
