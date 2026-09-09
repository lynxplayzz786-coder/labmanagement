# 🎨 Design

## UI Pages List (Complete)

| # | Page | Route | Access |
|---|------|-------|--------|
| 1 | Login | `/login/` | All (unauthenticated) |
| 2 | Register | `/register/` | All (unauthenticated) |
| 3 | Admin Dashboard | `/dashboard/` | Admin |
| 4 | Staff Dashboard | `/dashboard/` | Lab Staff |
| 5 | Student/Faculty Dashboard | `/dashboard/` | Student, Faculty |
| 6 | Equipment List | `/equipment/` | All (authenticated) |
| 7 | Equipment Detail | `/equipment/<id>/` | All |
| 8 | Add/Edit Equipment | `/equipment/add/` | Admin only |
| 9 | QR Code Page | `/equipment/<id>/qr/` | Admin, Staff |
| 10 | New Booking Request | `/bookings/new/` | Student, Faculty |
| 11 | My Bookings | `/bookings/` | Student, Faculty |
| 12 | Manage Bookings | `/bookings/manage/` | Staff, Admin |
| 13 | Return Equipment Form | `/bookings/<id>/return/` | Staff |
| 14 | Reports | `/reports/` | Admin |
| 15 | User Management | `/admin/` | Admin (Django admin) |

---

## Dashboard Layouts

### Admin Dashboard
```
┌─────────────────────────────────────────────────────┐
│   HEADER: Logo | Nav Links | User Avatar + Logout   │
├──────────────┬──────────────────────────────────────┤
│              │  ┌──────┐ ┌──────┐ ┌──────┐ ┌────┐ │
│   SIDEBAR    │  │Total │ │Avail │ │Rented│ │Mnt.│ │
│              │  │ 250  │ │ 180  │ │  50  │ │ 20 │ │
│  Dashboard   │  └──────┘ └──────┘ └──────┘ └────┘ │
│  Equipment   │  ┌─────────────┐   ┌──────────────┐ │
│  Bookings    │  │  Pie Chart  │   │  Line Chart  │ │
│  Reports     │  │ (by Cat.)   │   │  (Monthly)   │ │
│  Users       │  └─────────────┘   └──────────────┘ │
│              │  ┌──────────────────────────────────┤ │
│              │  │  Recent Pending Booking Requests │ │
└──────────────┴──┴──────────────────────────────────┘
```

### Staff Dashboard
```
┌─────────────────────────────────────────────────────┐
│                    HEADER                           │
├──────────────┬──────────────────────────────────────┤
│   SIDEBAR    │  ┌────────┐  ┌──────────┐  ┌──────┐ │
│              │  │Pending │  │ Issued   │  │Today │ │
│  Dashboard   │  │   12   │  │   35     │  │  5   │ │
│  Bookings    │  └────────┘  └──────────┘  └──────┘ │
│  Returns     │                                      │
│  Equipment   │  ┌──────────────────────────────────┐│
│              │  │   Today's Pending Requests Table ││
│              │  └──────────────────────────────────┘│
└──────────────┴──────────────────────────────────────┘
```

### Student / Faculty Dashboard
```
┌─────────────────────────────────────────────────────┐
│                    HEADER                           │
├──────────────┬──────────────────────────────────────┤
│   SIDEBAR    │  ┌──────────┐  ┌──────────┐          │
│              │  │My Active │  │ Pending  │          │
│  Dashboard   │  │Bookings 3│  │ Requests │          │
│  Equipment   │  └──────────┘  └──────────┘          │
│  My Bookings │                                      │
│              │  ┌──────────────────────────────────┐│
│              │  │      My Recent Bookings          ││
│              │  └──────────────────────────────────┘│
└──────────────┴──────────────────────────────────────┘
```

---

## Database Schema — Final (Fixed)

### Table 1: CustomUser
```sql
CustomUser                              -- Extends Django AbstractUser
------------------------------------
id                  PK  AUTO
username            VARCHAR(150)  UNIQUE
email               VARCHAR(254)  UNIQUE
first_name          VARCHAR(100)
last_name           VARCHAR(100)
role                ENUM('admin','staff','faculty','student')
phone               VARCHAR(15)   NULL
department          VARCHAR(100)  NULL
enrollment_no       VARCHAR(20)   NULL   -- Only for students
is_active           BOOLEAN       DEFAULT TRUE
date_joined         DATETIME      AUTO
```

### Table 2: Category
```sql
Category
------------------------------------
id                  PK  AUTO
name                VARCHAR(100)  UNIQUE   -- e.g., "Microcontroller"
description         TEXT          NULL
created_at          DATETIME      AUTO
```

### Table 3: Lab
```sql
Lab
------------------------------------
id                  PK  AUTO
name                VARCHAR(100)  UNIQUE   -- e.g., "IoT Lab"
location            VARCHAR(200)  NULL     -- e.g., "Block B, Room 201"
capacity            INT           NULL
is_active           BOOLEAN       DEFAULT TRUE
```

### Table 4: Equipment (Core)
```sql
Equipment
------------------------------------
id                  PK  AUTO
asset_id            VARCHAR(20)   UNIQUE   -- e.g., LAB-ARD-001 (auto-generated)
name                VARCHAR(200)
category_id         FK → Category
lab_id              FK → Lab
description         TEXT          NULL
quantity            INT           -- Total units
available_quantity  INT           -- Currently available units
status              ENUM('available','unavailable')
purchase_date       DATE          NULL
image               ImageField    NULL     -- stored in media/equipment/
qr_code             ImageField    NULL     -- stored in media/qrcodes/
created_at          DATETIME      AUTO
updated_at          DATETIME      AUTO

-- NOTE: No `condition` field here. Condition is tracked per-booking in IssueLog.
-- status becomes 'unavailable' only if available_quantity = 0.
```

### Table 5: Booking
```sql
Booking
------------------------------------
id                  PK  AUTO
booking_ref         VARCHAR(20)   UNIQUE   -- Auto: BK-{YYYY}-{0001} e.g., BK-2026-0001
requester_id        FK → CustomUser        -- student OR faculty
equipment_id        FK → Equipment
quantity            INT
request_date        DATE          AUTO     -- date booking was submitted
required_from       DATE                   -- equipment needed from
required_till       DATE                   -- equipment needed till
status              ENUM('pending','approved','rejected','issued','completed')
approved_by         FK → CustomUser  NULL  -- staff/admin who approved
approved_at         DATETIME        NULL
notes               TEXT            NULL   -- student's note
rejection_reason    TEXT            NULL   -- staff's rejection note
created_at          DATETIME        AUTO
updated_at          DATETIME        AUTO
```

### Table 6: IssueLog
```sql
IssueLog                                 -- Tracks Issue + Return for a Booking
------------------------------------
id                  PK  AUTO
booking_id          FK → Booking         UNIQUE  -- one IssueLog per Booking
issued_by           FK → CustomUser              -- staff who issued
issued_at           DATETIME
expected_return     DATE                         -- = booking.required_till
actual_return       DATETIME            NULL
returned_to         FK → CustomUser     NULL     -- staff who received return
condition_on_return ENUM('good','damaged','lost')  NULL
remarks             TEXT                NULL
is_overdue          BOOLEAN   (computed: actual_return > expected_return)
```

### Table 7: Maintenance
```sql
Maintenance
------------------------------------
id                  PK  AUTO
equipment_id        FK → Equipment
issue_log_id        FK → IssueLog       NULL     -- which return triggered it
reported_by         FK → CustomUser
issue_description   TEXT
status              ENUM('pending','in_progress','resolved')
created_at          DATETIME      AUTO
resolved_at         DATETIME      NULL
resolved_by         FK → CustomUser  NULL
```

---

## Key Business Logic Rules

```
Rule 1:  available_quantity can NEVER go below 0
Rule 2:  Student cannot book quantity > available_quantity
Rule 3:  Booking status flow is ONE-WAY (no going back)
         pending → approved/rejected → issued → completed
Rule 4:  On ISSUE   → available_quantity -= booking.quantity
Rule 5:  On RETURN (good) → available_quantity += booking.quantity
Rule 6:  On RETURN (damaged/lost) → Maintenance record created
                                 → available_quantity NOT updated
         (restored only after Maintenance.status = 'resolved')
Rule 7:  booking_ref auto-generated on Booking.save()
         Format: BK-{YEAR}-{4-digit-sequence}  e.g., BK-2026-0001
Rule 8:  asset_id auto-generated on Equipment.save()
         Format: LAB-{CATEGORY_CODE}-{3-digit-seq}  e.g., LAB-ARD-001
Rule 9:  If actual_return > expected_return → flag as overdue
```

---

## Color Palette & UI Style

```
Background:     #f0f2f5   (light grey — page bg)
Sidebar:        #1e2a3a   (dark navy)
Sidebar text:   #a8b8cc   (muted blue-grey)
Active link:    #4f8ef7   (bright blue)
Primary btn:    #4f8ef7
Success:        #22c55e   (green — available)
Warning:        #f59e0b   (amber — issued/pending)
Danger:         #ef4444   (red — maintenance/damaged)
Text (main):    #1e293b
Text (muted):   #64748b
Card bg:        #ffffff
Font:           Poppins (Google Fonts)
```

---

## Equipment Asset ID Format

```
LAB - [CATEGORY_CODE] - [3-DIGIT-SEQUENCE]

Category Code Mapping:
  ARD  → Arduino
  RPi  → Raspberry Pi
  OSC  → Oscilloscope
  MLT  → Multimeter
  NET  → Networking Equipment
  PRJ  → Projector
  SEN  → Sensors
  CBL  → Cables

Examples:
  LAB-ARD-001  → Arduino Uno (1st Arduino)
  LAB-ARD-002  → Arduino Mega (2nd Arduino entry)
  LAB-RPi-001  → Raspberry Pi 4
  LAB-OSC-001  → Oscilloscope
```

---

## Booking Reference Format

```
BK - {YEAR} - {4-digit-sequence}

Examples:
  BK-2026-0001  → First booking of year 2026
  BK-2026-0012  → 12th booking

Auto-generated in Booking.save() using:
  - Filter bookings of current year
  - Count + 1 → pad to 4 digits
```
