# 🧠 Agent Memory

*This file is my (AI's) memory. Updated after every major session.*

---

## Project Snapshot

| Field | Value |
|-------|-------|
| **Project** | BCA_29 — Lab Equipment Rental & Management System |
| **Supervisor** | Ms. Manisha Chawla |
| **Stack** | Python 3.11 + Django 4.2 LTS + MySQL 8.0 + Bootstrap 5.3 + Chart.js |
| **Current Phase** | 🎉 ALL PHASES COMPLETE — Project Ready for Submission |

---

## Session History

### Session 1 — [2026-08-13] Morning
- User asked to set up project tracking files
- Created 6 core documentation files in `project_docs/`

### Session 2 — [2026-08-13]
- User shared full BCA_29 requirement sheet and AI-generated plan
- Updated all 6 files with complete project details
- Phase 1 marked complete

### Session 7 — [2026-08-15 night]
- Phase 10: Documentation — COMPLETE ✅
  - README.md — Setup guide, credentials, structure, business rules
  - project_report.md — Full 7-chapter college report (ER, DFD, Schema, Test Cases, References)
  - viva_qa.md — 20+ detailed Q&A + quick-fire table for viva preparation
- **🎉 PROJECT 100% COMPLETE — All 10 phases done!**

### Session 6 — [2026-08-15 eve]
- Phase 9: Testing + Bug Fixes + Final Polish — COMPLETE ✅
  - Fixed booking_form missing `today` context bug
  - Custom 404 / 403 / 500 error pages
  - CSS micro-animations: fadeInUp, pulse badge, shrink-bar timer, sidebar slide
  - Print styles for reports
  - 12/12 URLs verified resolving correctly
- Phase 8: User Profile + Maintenance Module — COMPLETE ✅
- **Next: Phase 10 — Documentation (README, viva prep, sample data export)**

### Session 5 — [2026-08-15 cont]
- Phase 7: Dashboards + Charts + Reports — COMPLETE ✅
  - Admin dashboard: 3 Chart.js charts (doughnut/line/bar), stat cards, alert banners
  - Staff dashboard: pending + active rentals side by side
  - Student dashboard: quick actions + featured equipment + recent bookings
  - Reports page: overdue list, equipment usage, maintenance records
- **Next: Phase 8 — QR Generation, Maintenance Management, User Profile**

### Session 4 — [2026-08-15]
- Phase 2: Django Setup + MySQL — COMPLETE ✅
- Phase 3: All 7 DB models + migrations + seed data — COMPLETE ✅
- Phase 4: Auth (login/register/logout + forms + decorators + 3 dashboard templates) — COMPLETE ✅
- Phase 5: Equipment Module (list+search+filter, detail, add/edit, delete, QR page) — COMPLETE ✅
- Server running at http://127.0.0.1:8000 with zero errors
- **Next: Phase 6 — Booking Module**

### Session 3 — [2026-08-13]
- Cross-check performed. Problems found:
  1. Phase order was wrong (UI before DB — fixed)
  2. Redundant `inventory` app — removed, merged into `equipment`
  3. `condition` field on Equipment table — logic flaw — removed
  4. `booking_ref` auto-generation was undefined — added to design + rules
  5. QR scanning was unrealistic — scoped to "generation only"
  6. Faculty role was missing — added as 4th role
  7. Student dashboard was missing — added
  8. Business logic rules were undefined — added 9 rules to design.md
- **All 6 files updated with fixes**
- **Phase 2 (Django Setup) next to execute**

---

## Current Phase
> **Phase 2 — Django Setup + MySQL Connection**
> Goal: `http://localhost:8000` running. MySQL connected. Base template ready.

---

## Confirmed Decisions (Locked)

| Decision | Value | Reason |
|----------|-------|--------|
| Backend | Django 4.2 LTS | Clean MVT, built-in admin |
| DB | MySQL 8.0 | Required per project sheet |
| Frontend | Bootstrap 5.3 | Fast dashboard dev |
| Rendering | Django Templates | No React/Vue needed for BCA project |
| Roles | admin, staff, faculty, student | 4 roles, not 3 |
| QR | Generation only (no scanning) | Browser scanning is complex |
| inventory app | REMOVED — merged into equipment | Avoids over-engineering |
| condition field | On IssueLog, NOT on Equipment | Per-booking condition, not per-item |

---

## Database Tables Quick Reference

| Table | Location | Key Fields |
|-------|----------|-----------|
| `CustomUser` | `accounts/models.py` | role ENUM(admin,staff,faculty,student) |
| `Category` | `equipment/models.py` | name |
| `Lab` | `equipment/models.py` | name, location |
| `Equipment` | `equipment/models.py` | asset_id (auto), available_quantity |
| `Booking` | `bookings/models.py` | booking_ref (auto), status (5 states) |
| `IssueLog` | `bookings/models.py` | condition_on_return, is_overdue |
| `Maintenance` | `bookings/models.py` | status (3 states) |

---

## Critical Business Rules (Never Forget)

1. `available_quantity` can NEVER go below 0
2. Student/Faculty cannot book more than `available_quantity`
3. Booking status is ONE-WAY: pending→approved/rejected→issued→completed
4. On ISSUE → `available_quantity -= qty`
5. On RETURN (good) → `available_quantity += qty`
6. On RETURN (damaged/lost) → create Maintenance → do NOT restore qty
7. `booking_ref` auto = `BK-{YEAR}-{4-digit-seq}` e.g., BK-2026-0001
8. `asset_id` auto = `LAB-{CAT_CODE}-{3-digit-seq}` e.g., LAB-ARD-001
9. If `actual_return > expected_return` → flag `is_overdue = True`

---

## Django Apps Structure

```
accounts/     → CustomUser, login, register, logout, role decorators
equipment/    → Category, Lab, Equipment, CRUD, QR, search/filter
bookings/     → Booking, IssueLog, Maintenance, full lifecycle
dashboard/    → Role-based dashboards, charts, reports
```

---

## Pending / Open Questions

- [ ] Does supervisor want PDF report export? (Currently OUT of scope)
- [ ] Email notifications on approval? (Currently OUT of scope)
- [ ] Is `faculty` allowed to approve bookings? (Current: NO — only staff/admin)

---

## Phase 2 Checklist (What to do next session)

```
1. python --version  (check 3.11+)
2. mysql --version   (check 8.0+)
3. mkdir LabManagement → cd LabManagement
4. python -m venv venv
5. venv\Scripts\activate
6. pip install django==4.2.16 mysqlclient pillow qrcode django-crispy-forms crispy-bootstrap5
7. django-admin startproject lab_management .
8. python manage.py startapp accounts
9. python manage.py startapp equipment
10. python manage.py startapp bookings
11. python manage.py startapp dashboard
12. Configure settings.py (DATABASES, INSTALLED_APPS, STATIC, MEDIA, CRISPY)
13. CREATE DATABASE lab_management_db CHARACTER SET utf8mb4;
14. python manage.py migrate
15. python manage.py runserver → verify localhost:8000 works
16. Create base.html with Bootstrap + Font Awesome + Poppins
17. git init → git add . → git commit -m "Initial Django setup"
```
