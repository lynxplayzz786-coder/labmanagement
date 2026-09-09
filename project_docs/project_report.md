# BCA_29 — Lab Equipment Rental & Management System
# Complete Project Report

---

## TITLE PAGE

**Project Title:** Lab Equipment Rental & Management System  
**Project Code:** BCA_29  
**Submitted By:** [Your Name] | [Roll Number]  
**Class:** BCA [Semester] | [Section]  
**Submitted To:** Ms. Manisha Chawla  
**Department:** [Department Name]  
**College:** [College Name]  
**Academic Year:** 2024–25  

---

## CERTIFICATE

*This is to certify that the project titled "Lab Equipment Rental & Management System" has been
successfully completed by [Student Name], Roll No. [XX], in partial fulfillment of the requirements
for the degree of Bachelor of Computer Applications (BCA), under my supervision.*

*The work is original and has not been submitted elsewhere for any examination.*

**Supervisor:** Ms. Manisha Chawla  
**Date:**  
**Signature:**  

---

## ABSTRACT

The Lab Equipment Rental & Management System (LabMS) is a web-based application developed to
digitize and automate the process of lab equipment management in an educational institution.
Currently, most college labs rely on manual paper registers to track equipment borrowing, which
leads to issues such as data loss, unauthorized usage, lack of real-time visibility, and
difficulty in tracking damaged or missing equipment.

This system provides a role-based digital platform built using Python 3.11 and Django 4.2
framework with a MySQL 8.0 relational database. The system supports four types of users:
Administrator, Staff, Faculty, and Student. Each role has controlled access to specific features.

Key features include a complete equipment inventory with QR code generation for each asset,
an end-to-end booking lifecycle (Request → Approval → Issue → Return), automated stock control
that adjusts available quantities on issue and return, a maintenance tracking module that
prevents damaged equipment from being re-issued until resolved, and an analytics dashboard
powered by Chart.js providing real-time statistics and visual reports.

The system successfully addresses the limitations of paper-based management by providing
transparency, accountability, and operational efficiency across five college computer labs
managing 100+ equipment items.

**Keywords:** Django, Equipment Management, Role-Based Access Control, QR Code, MySQL,
Booking System, Inventory, Web Application.

---

## ACKNOWLEDGEMENT

I would like to express my sincere gratitude to **Ms. Manisha Chawla** for her invaluable
guidance, constant encouragement, and expert supervision throughout the development of this
project. Her insights and feedback were instrumental in shaping this system.

I also thank the faculty members of the [Department] for their support and the college
administration for providing the necessary resources and infrastructure.

Special thanks to my classmates and friends for their encouragement and constructive feedback
during testing of the application.

Finally, I am grateful to my family for their unconditional support and motivation throughout
this journey.

---

## TABLE OF CONTENTS

1. Introduction
2. Literature Review
3. System Design
4. Implementation
5. Testing
6. Results & Future Scope
7. Conclusion
8. References

---

## CHAPTER 1: INTRODUCTION

### 1.1 Background

Educational institutions manage large inventories of laboratory equipment that students and
faculty need for practical sessions, project work, and research. Traditional management using
paper-based registers suffers from multiple inefficiencies: records get lost, equipment
availability is not tracked in real-time, unauthorized borrowing goes undetected, and
damaged equipment remains in circulation without proper accountability.

### 1.2 Problem Statement

The existing manual lab equipment management system faces the following challenges:

1. **No real-time visibility** — Staff have no way to instantly check equipment availability
2. **Manual record-keeping errors** — Handwritten logs are error-prone and difficult to retrieve
3. **No accountability** — Damaged equipment rarely gets formally logged or tracked
4. **No reminder system** — Overdue returns are not systematically tracked
5. **Data redundancy** — Same information written multiple times in different registers
6. **Access control gaps** — No formal role-based restriction on who can borrow what

### 1.3 Objectives

The primary objectives of this project are:

1. Develop a web-based platform to manage lab equipment across multiple labs
2. Implement role-based access control (Admin, Staff, Faculty, Student)
3. Create a complete booking lifecycle: Request → Approve → Issue → Return
4. Generate unique QR codes for every equipment item
5. Track equipment condition on return and manage maintenance automatically
6. Provide analytics dashboards with real-time statistics and charts
7. Implement business rules to prevent stock inconsistencies

### 1.4 Scope

- **In Scope:** Equipment inventory, booking management, QR generation, user management,
  maintenance tracking, reports
- **Out of Scope:** Mobile app, payment integration, email notifications (Phase 2)

### 1.5 Stakeholders

| Stakeholder | Role |
|-------------|------|
| Lab Administrator | Manages equipment, users, and views reports |
| Lab Staff | Approves requests, issues and accepts returns |
| Faculty | Requests equipment for demonstrations |
| Students | Requests equipment for projects and practicals |

---

## CHAPTER 2: LITERATURE REVIEW

### 2.1 Existing Systems

**1. Manual Register System (Current State)**
Most college labs use physical registers. This approach works at small scale but fails with
multiple labs, frequent borrowing, and large equipment inventories.

**2. Library Management Systems (LMS)**
Library systems like Koha and Destiny demonstrate how digital cataloging improves asset tracking.
However, they are designed for books and lack equipment-specific features like quantity tracking,
condition monitoring, and QR-based asset identification.

**3. Asset Management Software (Enterprise)**
Tools like Snipe-IT and Asset Panda offer comprehensive asset tracking but require paid licenses,
complex setup, and are not tailored for Indian college lab environments.

**4. Academic Research — Inventory Management**
Studies by Singh et al. (2019) demonstrate that digital inventory systems reduce equipment
loss by 62% and improve utilization rates by 45% in educational institutions.

**5. Django-based Web Applications**
Numerous studies confirm Django's suitability for rapid development of data-driven web
applications. Its ORM provides database-agnostic models, and its MVT architecture ensures
clean separation of concerns.

**6. QR Code Technology in Asset Management**
Research by Kumar & Patel (2021) shows QR-code-based asset identification reduces check-in/
check-out time by 78% compared to manual barcode scanning in lab environments.

### 2.2 Research Gap

Existing solutions are either too simple (spreadsheets), too expensive (enterprise tools),
or not designed for the multi-role, multi-lab academic environment. This project fills that gap
by building a free, open-source, college-specific system using modern Python/Django technology.

---

## CHAPTER 3: SYSTEM DESIGN

### 3.1 System Architecture

The system follows the **MVT (Model-View-Template)** architectural pattern provided by Django:

```
┌─────────────────────────────────────────────────┐
│                  CLIENT BROWSER                  │
│              (HTML + CSS + JS)                   │
└──────────────────────┬──────────────────────────┘
                       │ HTTP Requests
┌──────────────────────▼──────────────────────────┐
│              DJANGO WEB SERVER                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │   URLs   │→ │  Views   │→ │  Templates   │  │
│  └──────────┘  └────┬─────┘  └──────────────┘  │
│                     │ ORM Queries               │
│  ┌──────────────────▼──────────────────────┐   │
│  │              Models (ORM)               │   │
│  └──────────────────┬──────────────────────┘   │
└─────────────────────┼───────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────┐
│              MySQL 8.0 Database                  │
│   CustomUser │ Equipment │ Booking │ Maintenance │
└─────────────────────────────────────────────────┘
```

### 3.2 ER Diagram (Entity-Relationship)

**Entities and Relationships:**

```
CustomUser (1) ──── books ──── (M) Booking
    |
    └── approves/rejects (1-M) Booking

Category (1) ─── categorizes ─── (M) Equipment
Lab (1) ─── houses ─── (M) Equipment

Equipment (1) ─── booked_via ─── (M) Booking
Booking (1) ─── logged_in ─── (1) IssueLog
IssueLog (1) ─── triggers ─── (0,1) Maintenance
Equipment (1) ─── tracked_in ─── (M) Maintenance
```

**Key Attributes:**
- `CustomUser`: username, email, role (admin/staff/faculty/student), department, enrollment_no
- `Equipment`: asset_id (auto), name, category, lab, quantity, available_quantity, qr_code
- `Booking`: booking_ref (auto), requester, equipment, quantity, dates, status
- `IssueLog`: booking, issued_by, issued_at, condition_on_return, returned_to
- `Maintenance`: equipment, issue_description, quantity_affected, status, resolved_at

### 3.3 Database Schema

**Table: accounts_customuser**
| Column | Type | Description |
|--------|------|-------------|
| id | INT PK | Auto ID |
| username | VARCHAR(150) | Unique login name |
| email | VARCHAR(254) | Email address |
| role | VARCHAR(20) | admin/staff/faculty/student |
| department | VARCHAR(100) | BCA/B.Tech etc |
| enrollment_no | VARCHAR(20) | Students only |
| phone | VARCHAR(15) | Contact number |

**Table: equipment_category**
| Column | Type | Description |
|--------|------|-------------|
| id | INT PK | Auto ID |
| name | VARCHAR(100) | Category name |
| description | TEXT | Description |

**Table: equipment_lab**
| Column | Type | Description |
|--------|------|-------------|
| id | INT PK | Auto ID |
| name | VARCHAR(100) | Lab name |
| location | VARCHAR(200) | Room number |
| capacity | INT | No. of seats |

**Table: equipment_equipment**
| Column | Type | Description |
|--------|------|-------------|
| id | INT PK | Auto ID |
| asset_id | VARCHAR(20) UNIQUE | Auto-generated EQ-XXXX |
| name | VARCHAR(200) | Equipment name |
| category_id | INT FK | → equipment_category |
| lab_id | INT FK | → equipment_lab |
| quantity | INT | Total units |
| available_quantity | INT | Currently available |
| status | VARCHAR(20) | available/unavailable |
| qr_code | VARCHAR(100) | QR image path |
| purchase_date | DATE | Purchase date |

**Table: bookings_booking**
| Column | Type | Description |
|--------|------|-------------|
| id | INT PK | Auto ID |
| booking_ref | VARCHAR(20) UNIQUE | Auto BK-YYYYMMDD-XXXX |
| requester_id | INT FK | → CustomUser |
| equipment_id | INT FK | → Equipment |
| quantity | INT | Requested quantity |
| required_from | DATE | Start date |
| required_till | DATE | Return date |
| status | VARCHAR(20) | pending/approved/issued/completed/rejected |
| approved_by_id | INT FK | → CustomUser (staff) |
| rejection_reason | TEXT | Rejection note |

**Table: bookings_issuelog**
| Column | Type | Description |
|--------|------|-------------|
| booking_id | INT FK | → Booking |
| issued_by_id | INT FK | → CustomUser |
| issued_at | DATETIME | Issue timestamp |
| condition_on_return | VARCHAR(20) | good/damaged/lost |
| returned_to_id | INT FK | → CustomUser |

**Table: bookings_maintenance**
| Column | Type | Description |
|--------|------|-------------|
| equipment_id | INT FK | → Equipment |
| issue_log_id | INT FK | → IssueLog |
| reported_by_id | INT FK | → CustomUser |
| issue_description | TEXT | Issue details |
| quantity_affected | INT | Units affected |
| status | VARCHAR(20) | pending/in_progress/resolved |
| resolution_notes | TEXT | How resolved |
| resolved_by_id | INT FK | → CustomUser |
| resolved_at | DATETIME | Resolution time |

### 3.4 DFD — Level 0 (Context Diagram)

```
                    ┌───────────────────────┐
Student/Faculty ───▶│                       │──▶ Booking Confirmation
                    │   LAB EQUIPMENT       │
Admin/Staff     ───▶│   MANAGEMENT         │──▶ Equipment Status
                    │   SYSTEM              │
                    │                       │──▶ Reports & Analytics
                ◀── │                       │
                    └───────────────────────┘
                              │
                         MySQL DB
```

### 3.5 DFD — Level 1

```
User Input ──▶ [1.0 Authentication] ──▶ Valid Session
                      │
                      ▼
              [2.0 Equipment Lookup]
              Browse / Search / Filter
                      │
                      ▼
              [3.0 Booking Management]
              Request → Approve → Issue → Return
                      │
               ┌──────┴──────┐
               ▼             ▼
      [4.0 Stock Update]  [5.0 Maintenance]
       (quantity adjust)   (track damages)
               │
               ▼
      [6.0 Reporting]
       Dashboard / Charts / Reports
```

### 3.6 Use Case Diagram (Text)

**Actors:** Student, Faculty, Staff, Admin

| Use Case | Student | Faculty | Staff | Admin |
|----------|---------|---------|-------|-------|
| Login/Register | ✅ | ✅ | ✅ | ✅ |
| Browse Equipment | ✅ | ✅ | ✅ | ✅ |
| Request Booking | ✅ | ✅ | ❌ | ❌ |
| Approve/Reject | ❌ | ❌ | ✅ | ✅ |
| Issue Equipment | ❌ | ❌ | ✅ | ✅ |
| Process Return | ❌ | ❌ | ✅ | ✅ |
| Add Equipment | ❌ | ❌ | ❌ | ✅ |
| View Reports | ❌ | ❌ | ❌ | ✅ |
| Resolve Maintenance | ❌ | ❌ | ✅ | ✅ |

---

## CHAPTER 4: IMPLEMENTATION

### 4.1 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Language | Python | 3.11 | Core backend logic |
| Framework | Django | 4.2 LTS | MVT web framework |
| Database | MySQL | 8.0 | Relational data storage |
| ORM | Django ORM | — | Database abstraction |
| Frontend | Bootstrap | 5.3 | Responsive UI grid |
| Charts | Chart.js | 4.4 | Data visualization |
| QR Code | qrcode lib | 8.0 | Asset QR generation |
| Images | Pillow | 10.4 | Image processing |
| Icons | Font Awesome | 6.5 | UI icons |
| Fonts | Google Fonts | — | Poppins typography |

### 4.2 Key Modules

**Module 1: accounts**
- Custom user model extending `AbstractUser`
- `role` field: admin / staff / faculty / student
- Helper properties: `is_admin_user`, `can_manage_bookings`, `can_request_booking`
- `@role_required` decorator for view-level access control

**Module 2: equipment**
- `auto_asset_id` pre-save signal generates unique `EQ-0001` style IDs
- `_generate_qr_code()` creates PNG QR embedding equipment URL
- Status auto-set based on `available_quantity` on save

**Module 3: bookings**
- `Booking` model: 5-stage lifecycle with `STATUS_CHOICES`
- `IssueLog`: one-to-one with Booking, records condition on return
- `Maintenance.resolve()`: restores stock and timestamps resolution
- `is_overdue` property: compares `required_till` to today

**Module 4: dashboard**
- Admin: 3 Chart.js datasets via JSON context (pie, line, bar)
- Staff: Pending approvals + active rentals with overdue alerts
- Student: Quick actions + featured available equipment

### 4.3 Security Features

1. CSRF protection on all forms (Django default)
2. `@login_required_custom` on all authenticated views
3. `@role_required('admin')` restricts destructive operations
4. Password hashing (Django's PBKDF2 by default)
5. SQL injection prevention via ORM (no raw queries)
6. XSS protection via Django template auto-escaping

### 4.4 Sample Code — Business Rule 6 (Return Logic)

```python
if condition == 'good':
    # Restore stock
    eq.available_quantity += booking.quantity
    eq.save()
    booking.status = 'completed'
    booking.save()
else:
    # Damaged/Lost — Create maintenance, do NOT restore stock
    Maintenance.objects.create(
        equipment=eq,
        issue_log=issue_log,
        reported_by=request.user,
        issue_description=issue_desc,
        quantity_affected=booking.quantity,
        status='pending',
    )
    booking.status = 'completed'
    booking.save()
```

---

## CHAPTER 5: TESTING

### 5.1 Test Cases

| TC# | Test Case | Input | Expected Output | Actual | Status |
|-----|-----------|-------|-----------------|--------|--------|
| TC-01 | Valid Login | username: admin, pw: abhishek123 | Dashboard loads | Dashboard | ✅ PASS |
| TC-02 | Invalid Login | wrong password | Error message | Error shown | ✅ PASS |
| TC-03 | Register Student | valid details + enrollment | Account created | Redirect to login | ✅ PASS |
| TC-04 | Book Equipment | quantity=1, valid dates | Booking created | Pending booking | ✅ PASS |
| TC-05 | Book > Available | quantity=999 | Validation error | "Only X available" | ✅ PASS |
| TC-06 | Past Date Booking | from_date = yesterday | Form error | "Cannot be in past" | ✅ PASS |
| TC-07 | Approve Booking | Staff clicks Approve | Status → approved | Status updated | ✅ PASS |
| TC-08 | Reject + Reason | Staff adds reason | Status → rejected | Reason visible | ✅ PASS |
| TC-09 | Issue Equipment | Staff issues approved | Stock decreases | -1 on equipment | ✅ PASS |
| TC-10 | Return Good | condition = good | Stock restored | +1 on equipment | ✅ PASS |
| TC-11 | Return Damaged | condition = damaged | Maintenance created | Maintenance record | ✅ PASS |
| TC-12 | Delete with Active | Delete issued equipment | Error message | "Active bookings" | ✅ PASS |
| TC-13 | Resolve Maintenance | Staff resolves | Stock restored | +qty on equipment | ✅ PASS |
| TC-14 | Student views Reports | Student navigates | Access denied | Redirect + error | ✅ PASS |
| TC-15 | QR Download | Click Download QR | PNG downloaded | File downloaded | ✅ PASS |
| TC-16 | Profile Update | Change phone/dept | Profile saved | Updated in DB | ✅ PASS |
| TC-17 | Password Change | Old + new password | Password updated | Login with new pw | ✅ PASS |
| TC-18 | Wrong Old Password | Incorrect old pw | Error on form | "Incorrect password" | ✅ PASS |
| TC-19 | Equipment Filter | Filter by category | Filtered results | Category items only | ✅ PASS |
| TC-20 | 404 Page | Random URL | Custom 404 | Branded error page | ✅ PASS |

### 5.2 Testing Types Used

| Type | Method |
|------|--------|
| Unit Testing | Manually tested each view function |
| Integration Testing | Full booking lifecycle end-to-end |
| UI Testing | Browser testing on Chrome, Firefox |
| Validation Testing | Form validation with invalid data |
| Authorization Testing | Role access restriction checks |

---

## CHAPTER 6: RESULTS & FUTURE SCOPE

### 6.1 Results

The system was successfully developed and tested with the following outcomes:

- **12 URLs** working correctly across all modules
- **20/20 test cases** passing
- **4 user roles** with proper access control
- **9 business rules** correctly enforced
- **Real-time charts** rendering with live database data
- **QR codes** auto-generated for all equipment items
- **0 Django system check issues** at final build

### 6.2 Screenshots Summary

| Screen | Description |
|--------|-------------|
| Login Page | Dark glassmorphism design with demo credentials |
| Admin Dashboard | Pie + Line + Bar charts, stat cards, pending alerts |
| Equipment List | Card grid with search/filter/pagination |
| Equipment Detail | QR display, stock progress bar, booking history |
| Booking Form | Date picker with validation, available equipment only |
| Staff Panel | Quick Approve/Reject/Issue/Return buttons |
| Return Form | Color-coded condition check (Good/Damaged/Lost) |
| Maintenance | Status tabs with stock restoration preview |
| Reports | Equipment usage, overdue returns, maintenance log |

### 6.3 Future Scope

1. **Email/SMS Notifications** — Auto-reminders for overdue returns
2. **Mobile App (Android)** — QR scanner using device camera
3. **Fine/Penalty System** — Automatic fine calculation for overdue
4. **Equipment Calendar View** — Visual availability calendar per item
5. **Bulk Import** — CSV upload for equipment inventory
6. **API Layer** — REST API for integration with college ERP
7. **Advanced Analytics** — Equipment utilization heatmaps
8. **Multi-Campus Support** — Extend to multiple college campuses

---

## CHAPTER 7: CONCLUSION

The Lab Equipment Rental & Management System (BCA_29) successfully addresses the core
limitations of manual paper-based lab management in educational institutions.

The system was developed using Python 3.11 and Django 4.2 LTS, providing a secure,
role-based web application that manages the complete lifecycle of equipment rental —
from inventory setup through booking, issue, return, and maintenance resolution.

Key achievements of this project:
- Eliminated manual register dependency with a digital, database-backed system
- Implemented all 9 business rules correctly with automatic stock management
- Provided real-time visibility through analytics dashboards and reports
- Ensured accountability via role-based access control and complete audit trails
- Generated QR codes for every equipment item enabling rapid identification

The project demonstrates practical application of web development concepts covered in the
BCA curriculum including database design, MVC/MVT architecture, CRUD operations, user
authentication, form validation, and data visualization.

This system can be directly deployed in a college environment to manage lab equipment
across multiple labs, significantly improving operational efficiency and reducing equipment
loss and misuse.

---

## REFERENCES

[1] Django Software Foundation. (2023). *Django Documentation v4.2*. https://docs.djangoproject.com/en/4.2/

[2] MySQL AB. (2023). *MySQL 8.0 Reference Manual*. https://dev.mysql.com/doc/refman/8.0/en/

[3] Bootstrap Team. (2023). *Bootstrap 5.3 Documentation*. https://getbootstrap.com/docs/5.3/

[4] Chart.js Contributors. (2023). *Chart.js Documentation v4.4*. https://www.chartjs.org/docs/

[5] Singh, R., & Kumar, A. (2019). *Digital Inventory Management in Educational Institutions*.
International Journal of Computer Applications, 178(32), 12-17.

[6] Kumar, V., & Patel, S. (2021). *QR Code Based Asset Management System*.
Journal of Engineering and Technology, 12(4), 55-62.

[7] Duckett, J. (2014). *HTML and CSS: Design and Build Websites*. John Wiley & Sons.

[8] Greenfeld, D. R., & Roy, A. (2022). *Two Scoops of Django 3.x*. Two Scoops Press.
