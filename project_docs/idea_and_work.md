# 💡 Project Idea & Work

## Project Identity
| Field | Details |
|-------|---------|
| **Project ID** | BCA_29 |
| **Project Name** | Lab Equipment Rental & Management System |
| **Supervisor** | Ms. Manisha Chawla |
| **SDG Goal** | SDG 4 – Quality Education, SDG 9 – Industry, Innovation & Infrastructure |

---

## Problem Statement
Educational institutions often manage laboratory equipment manually, leading to:
- Inefficient tracking
- Booking conflicts
- Delayed returns
- Equipment loss and misuse

An automated system can streamline equipment allocation and inventory management.

---

## Project Objectives
1. Automate equipment booking and tracking
2. Reduce equipment loss and misuse
3. Improve inventory management and utilization
4. Provide role-based access for Admin, Lab Staff, Faculty, and Students

---

## Core Idea

A college has:
- **5 Computer Labs**
- **100+ Equipment** (Oscilloscope, Multimeter, Arduino kits, Raspberry Pi, Projectors, Sensors, Networking equipment, Cables, etc.)

**Who can borrow?** → Students & Faculty
**Who manages?** → Lab Staff + Admin

System tracks the full lifecycle:

```
Equipment Added by Admin
         ↓
    Available in Stock
         ↓
Student/Faculty Submits Booking Request
         ↓
Staff/Admin Reviews → Approve / Reject
         ↓ (if Approved)
Staff Issues Equipment → Stock Decreases
         ↓
Student/Faculty Returns Equipment
         ↓
Staff checks Condition → Good / Damaged / Lost
         ↓
  Good → Stock Increases (Available Again)
  Damaged → Maintenance Flag → Stock NOT restored until fixed
```

---

## Core Feature Modules

| Module | Features | Who |
|--------|----------|-----|
| **Authentication** | Login / Register / Logout | All |
| **Roles** | Admin / Lab Staff / Faculty / Student | System |
| **Equipment** | Add / Edit / Delete / View / Search / Filter | Admin, All (view) |
| **Categories** | Electronics, Networking, Computing, Sensors, etc. | Admin |
| **Labs** | IoT Lab, Computer Lab 1-5, etc. | Admin |
| **Booking** | Submit booking request | Student / Faculty |
| **Approval** | Approve / Reject bookings | Staff / Admin |
| **Issue** | Mark equipment as issued | Staff |
| **Return** | Process return + condition check | Staff |
| **Dashboard** | Stats + Charts (role-based view) | All |
| **History** | Complete rental history | All (own data) |
| **Reports** | Equipment usage, maintenance, overdue | Admin |

---

## Confirmed Scope (Frozen)

### IN Scope (Must Build)
- [x] User authentication with 4 roles
- [x] Equipment CRUD with asset ID
- [x] Full booking lifecycle (request → issue → return)
- [x] Role-based dashboards
- [x] QR Code generation per equipment (NOT scanning — generation only)
- [x] Search and Filter on equipment
- [x] Maintenance tracking
- [x] Reports and charts

### OUT of Scope (Will NOT Build)
- ❌ QR Code scanning (browser-based scanning is complex — generation only)
- ❌ Email notifications (optional, only if time permits)
- ❌ PDF export of reports (optional, only if time permits)
- ❌ Mobile app
- ❌ Payment system

---

## Current Work Status
- [x] Phase 1 — Requirement Analysis complete
- [ ] Phase 2 — Django Setup + MySQL
- [ ] Phase 3 — Database Design + Models
- [ ] Phase 4 — Authentication Module
- [ ] Phase 5 — Equipment Module
- [ ] Phase 6 — Booking Module
- [ ] Phase 7 — Dashboard + Reports
- [ ] Phase 8 — UI Polish
- [ ] Phase 9 — Testing
- [ ] Phase 10 — Documentation
