# 🗓️ Project Phases

## Overview
Total Phases: **10**
Approach: **Foundation First → Features → Polish**

> ⚠️ Phase order is intentional and FIXED. Do NOT skip or reorder.
> Each phase must be complete and tested before moving to the next.

---

## ✅ Phase 1 — Requirement Analysis (DONE)
**Goal:** Freeze scope, define everything before a single line of code.

- [x] Defined users and roles (Admin, Staff, Faculty, Student)
- [x] Confirmed feature list + frozen scope
- [x] Designed database schema (7 tables)
- [x] Defined booking workflow (state machine)
- [x] Defined business logic rules
- [x] Confirmed tech stack (Django + MySQL + Bootstrap)
- [x] Created all project documentation files

**Output:** All `project_docs/` files finalized.

---

## 🔄 Phase 2 — Django Setup + MySQL Connection (CURRENT)
**Goal:** Get a working Django project connected to MySQL, nothing more.

**Tasks:**
- [ ] Install Python 3.11+ (check: `python --version`)
- [ ] Install MySQL 8.0+ + MySQL Workbench
- [ ] Create project directory structure
- [ ] Create and activate virtual environment
- [ ] Install all packages from `requirements.txt`
- [ ] Start Django project: `django-admin startproject lab_management .`
- [ ] Create all apps: `accounts`, `equipment`, `bookings`, `dashboard`
- [ ] Register apps in `settings.py`
- [ ] Configure MySQL in `settings.py` (DATABASES block)
- [ ] Create MySQL database: `lab_management_db`
- [ ] Run `python manage.py migrate` (test connection)
- [ ] Run `python manage.py runserver` (test server runs)
- [ ] Create `base.html` with Bootstrap 5, Font Awesome, Poppins font
- [ ] Create `static/css/style.css` with custom variables
- [ ] Push to GitHub (initial commit)

**Output:** `http://localhost:8000` running Django default page. MySQL connected.

---

## Phase 3 — Database Design + Models + Migrations
**Goal:** Create all Django models exactly as per design.md schema.

**Tasks:**
- [ ] `accounts/models.py` → `CustomUser` model (extends AbstractUser, adds `role` field)
- [ ] `equipment/models.py` → `Category`, `Lab`, `Equipment` models
  - [ ] Auto asset_id generation in `Equipment.save()`
  - [ ] QR code generation hook in `Equipment.save()`
- [ ] `bookings/models.py` → `Booking`, `IssueLog`, `Maintenance` models
  - [ ] Auto booking_ref generation in `Booking.save()`
- [ ] Register all models in `admin.py` files
- [ ] Run `python manage.py makemigrations`
- [ ] Run `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Test via Django Admin: Add a Category, Lab, Equipment manually
- [ ] Verify auto-generated asset_id appears correctly

**Output:** All 7 tables created in MySQL. Verified in MySQL Workbench.

---

## Phase 4 — Authentication Module
**Goal:** Complete login, register, logout with role-based redirects.

**Tasks:**
- [ ] `accounts/forms.py` → `LoginForm`, `RegisterForm`
- [ ] `accounts/views.py` → `login_view`, `register_view`, `logout_view`
- [ ] `accounts/decorators.py` → `role_required(roles)` decorator
- [ ] `accounts/urls.py` → wire up login/register/logout
- [ ] `templates/accounts/login.html` → styled login page
- [ ] `templates/accounts/register.html` → styled register page
- [ ] Role-based redirect after login:
  - `admin` → admin dashboard
  - `staff` → staff dashboard
  - `student/faculty` → student dashboard
- [ ] Protect all views: unauthenticated → redirect to login
- [ ] Test: login as each role, check redirect

**Output:** Working auth. 3 roles redirect correctly. Unauthenticated users cannot access any page.

---

## Phase 5 — Equipment Module
**Goal:** Full CRUD for equipment with search, filter, and QR generation.

**Tasks:**
- [ ] `equipment/views.py`:
  - [ ] `equipment_list` (with pagination, search, filter)
  - [ ] `equipment_detail`
  - [ ] `equipment_add` (admin only)
  - [ ] `equipment_edit` (admin only)
  - [ ] `equipment_delete` (admin only)
  - [ ] `equipment_qr` (generate + show QR)
- [ ] `equipment/forms.py` → `EquipmentForm`, `CategoryForm`
- [ ] `equipment/utils.py` → QR code generator function
- [ ] Templates: `list.html`, `detail.html`, `add_edit.html`, `qr.html`
- [ ] Search: by name, asset_id
- [ ] Filter: by category, lab, status
- [ ] Pagination: 10 items per page
- [ ] Test: Add 5 equipment → verify asset_id, QR generated
- [ ] Test: Admin can edit/delete. Student can only view.

**Output:** Equipment list with working search/filter. QR code downloadable.

---

## Phase 6 — Booking Module
**Goal:** Full booking lifecycle — request → approve → issue → return.

**Tasks:**
- [ ] `bookings/views.py`:
  - [ ] `booking_request` (student/faculty)
  - [ ] `my_bookings` (student/faculty)
  - [ ] `manage_bookings` (staff/admin — pending list)
  - [ ] `approve_booking` (staff/admin)
  - [ ] `reject_booking` (staff/admin)
  - [ ] `issue_equipment` (staff)
  - [ ] `process_return` (staff)
- [ ] `bookings/forms.py` → `BookingForm`, `ReturnForm`
- [ ] Templates for all views
- [ ] Business logic in views:
  - [ ] Check `available_quantity >= requested_quantity` before booking
  - [ ] `available_quantity -= qty` on issue
  - [ ] `available_quantity += qty` on good return
  - [ ] Create `Maintenance` record on damaged/lost return
  - [ ] Auto `booking_ref` generation verified
- [ ] Test all 9 business rules from design.md

**Output:** Full booking lifecycle works end-to-end. All 9 rules enforced.

---

## Phase 7 — Dashboard + Reports Module
**Goal:** Role-based dashboards with live stats and charts.

**Tasks:**
- [ ] `dashboard/views.py`:
  - [ ] `admin_dashboard` → total assets, available, rented, maintenance + charts
  - [ ] `staff_dashboard` → pending, issued today
  - [ ] `student_dashboard` → my active bookings, pending requests
- [ ] Charts (Chart.js via JSON data from Django view):
  - [ ] Pie chart: equipment by category
  - [ ] Line chart: monthly bookings (last 6 months)
  - [ ] Bar chart: top 5 most booked equipment
- [ ] Reports page (admin only):
  - [ ] Equipment usage report (table)
  - [ ] Maintenance history
  - [ ] Overdue returns list
- [ ] Test: Charts render with real data

**Output:** All 3 dashboards live. Charts working. Reports page accessible.

---

## Phase 8 — UI Polish
**Goal:** Make the UI look premium and consistent across all pages.

**Tasks:**
- [ ] Finalize `base.html` (sidebar, navbar, breadcrumbs)
- [ ] Apply custom color palette from design.md
- [ ] Responsive sidebar (collapses on mobile)
- [ ] Consistent card styles, button styles across all pages
- [ ] Status badges: color-coded (pending=yellow, approved=blue, issued=orange, completed=green)
- [ ] Add page titles, meta descriptions for all pages
- [ ] Empty state UI (e.g., "No bookings yet" with icon)
- [ ] Flash messages (success/error after actions)
- [ ] Cross-browser test on Chrome + Firefox

**Output:** Visually polished, consistent UI ready for demo/viva.

---

## Phase 9 — Testing + Bug Fix
**Goal:** Systematically test all flows and fix bugs.

**Test Cases (Manual):**
- [ ] Student cannot book quantity > available_quantity (should show error)
- [ ] Student cannot access `/bookings/manage/` (should get 403/redirect)
- [ ] Admin can access all pages
- [ ] Available quantity cannot go negative
- [ ] Equipment returned twice → second return should fail (already completed)
- [ ] Damaged return → maintenance record created, qty NOT restored
- [ ] booking_ref is unique (no duplicates)
- [ ] asset_id is unique (no duplicates)
- [ ] Login with wrong password → proper error message
- [ ] Empty form submission → validation errors shown

**Output:** All test cases pass. No critical bugs.

---

## Phase 10 — Documentation (College Report)
**Goal:** Write complete project report for college submission.

**Report Sections:**
- [ ] Title Page
- [ ] Certificate
- [ ] Abstract (250-300 words)
- [ ] Acknowledgement
- [ ] Table of Contents
- [ ] Chapter 1: Introduction + Problem Statement + Objectives
- [ ] Chapter 2: Literature Review (5-6 references)
- [ ] Chapter 3: System Design
  - ER Diagram
  - DFD (Level 0 + Level 1)
  - Database Schema
  - System Architecture
- [ ] Chapter 4: Implementation + Screenshots
- [ ] Chapter 5: Testing (test cases table)
- [ ] Chapter 6: Results + Future Scope
- [ ] Chapter 7: Conclusion
- [ ] References (IEEE format)

**Output:** Complete Word/PDF report submitted to Ms. Manisha Chawla.

---

## Timeline (Realistic)

| Phase | Name | Estimated Time |
|-------|------|---------------|
| ✅ Phase 1 | Requirements | Done |
| 🔄 Phase 2 | Django Setup + MySQL | 1 day |
| Phase 3 | Models + Migrations | 1 day |
| Phase 4 | Authentication | 1-2 days |
| Phase 5 | Equipment Module | 2-3 days |
| Phase 6 | Booking Module | 3-4 days |
| Phase 7 | Dashboard + Reports | 2 days |
| Phase 8 | UI Polish | 1-2 days |
| Phase 9 | Testing | 1 day |
| Phase 10 | Documentation | 3-4 days |
| **Total** | | **~16-19 days** |
