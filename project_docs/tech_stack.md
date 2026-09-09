# ⚙️ Tech Stack

## Official Stack (As per BCA_29 Requirement Sheet)

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | HTML5 | Latest | Page Structure |
| **Frontend** | CSS3 | Latest | Styling |
| **Frontend** | JavaScript | ES6+ | Interactivity |
| **Frontend** | Bootstrap | 5.3 | Responsive UI Components |
| **Charts** | Chart.js | 4.x | Dashboard Graphs |
| **Icons** | Font Awesome | 6.x | UI Icons |
| **Fonts** | Google Fonts (Poppins) | Latest | Typography |
| **Backend** | Python | 3.11+ | Core Language |
| **Backend** | Django | 4.2 LTS | Web Framework |
| **Database** | MySQL | 8.0+ | Data Storage |
| **ORM** | Django ORM | (built-in) | DB Queries (no raw SQL) |
| **Auth** | Django Authentication | (built-in) | Login/Sessions/Roles |
| **QR Code** | `qrcode` + `Pillow` | Latest | Equipment QR Generation |
| **Forms** | django-crispy-forms | 2.x | Better form rendering |
| **IDE** | VS Code | Latest | Development |
| **Version Control** | Git + GitHub | Latest | Source Control |

---

## Why This Stack?

### ✅ Django (Python) — Why Not PHP/Laravel?
- Both allowed per requirement sheet
- Django chosen because:
  - Cleaner MVT architecture
  - Built-in Admin Panel (saves setup time)
  - Powerful ORM (no raw SQL needed)
  - Python is easier to debug with AI assistance
  - `django-crispy-forms` makes form UI fast

### ✅ MySQL — Why Not SQLite?
- SQLite is Django default but MySQL chosen because:
  - Required as per project sheet
  - Better for multi-user concurrent access
  - More realistic for a college management system
  - Proper FK constraints enforcement

### ✅ Bootstrap 5 — Why Not Tailwind?
- Bootstrap 5 has ready-made dashboard components
- Faster for forms, tables, modals, cards
- Well-known in college projects (easy to explain in viva)

### ✅ Django Templates — Why Not React/Vue?
- This is a BCA college project, not a SPA
- Django templates keep everything in one place
- No need for API layer — simpler architecture
- Faster to build and easier to explain

---

## Python Package Dependencies

```
# requirements.txt

Django==4.2.16
mysqlclient==2.2.4
Pillow==10.4.0
qrcode==7.4.2
django-crispy-forms==2.3
crispy-bootstrap5==2024.2
```

> **Note:** `mysqlclient` requires MySQL server installed on Windows.
> Alternative if mysqlclient fails: use `PyMySQL` instead.

---

## Frontend Libraries (via CDN — No npm needed)

```html
<!-- Bootstrap 5.3 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Chart.js 4.x -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- Font Awesome 6 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<!-- Google Fonts — Poppins -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## Development Environment Setup

```
OS:           Windows 10/11
IDE:          VS Code
Python:       3.11+ (from python.org)
pip:          bundled with Python
MySQL:        8.0+ (MySQL Community Server)
MySQL GUI:    MySQL Workbench (optional, for DB viewing)
Browser:      Chrome (for testing)
Git:          Git for Windows
```

---

## Installed VS Code Extensions (Recommended)

```
Python              (Microsoft)
Django              (Baptiste Darthenay)
SQLTools            (Matheus Teixeira) — view MySQL in VS Code
GitLens             (GitKraken)
Auto Rename Tag     (Jun Han)
Prettier            (Prettier)
```
