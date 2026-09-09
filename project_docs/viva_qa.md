# BCA_29 — Viva Questions & Answers

**Project:** Lab Equipment Rental & Management System  
**Prepared for:** Project Viva / Presentation  
**Supervisor:** Ms. Manisha Chawla

---

## SECTION 1: Basic Project Questions

**Q1. What is your project about? Explain in 2-3 lines.**

> My project "Lab Equipment Rental & Management System" is a web-based application that
> digitizes lab equipment borrowing in college. It allows students and faculty to request
> equipment online, and staff/admin to approve, issue, and track returns with automatic
> stock management and damage reporting.

---

**Q2. Why did you choose this project?**

> College labs currently use manual paper registers which are error-prone, slow, and
> don't provide real-time visibility. Equipment gets lost or damaged without accountability.
> This project solves those real-world problems by replacing paper with a digital system.

---

**Q3. Who are the users of your system?**

> The system has 4 types of users:
> 1. **Admin** — Full control: manages equipment, users, views reports
> 2. **Staff** — Approves bookings, issues equipment, processes returns
> 3. **Faculty** — Requests equipment for teaching
> 4. **Student** — Requests equipment for projects

---

**Q4. What is the tech stack you used?**

> - **Backend:** Python 3.11 + Django 4.2 LTS
> - **Database:** MySQL 8.0
> - **Frontend:** HTML5 + Bootstrap 5.3 + CSS3
> - **Charts:** Chart.js 4.4
> - **QR Code:** Python `qrcode` library
> - **Icons:** Font Awesome 6.5

---

## SECTION 2: Technical Questions

**Q5. What is Django? Why did you choose it?**

> Django is a high-level Python web framework that follows the MVT (Model-View-Template)
> pattern. I chose it because:
> - Built-in ORM (no raw SQL needed)
> - Admin panel out of the box
> - Strong security defaults (CSRF, XSS, SQL injection protection)
> - Fast development with less code
> - LTS (Long Term Support) version 4.2 — stable for production

---

**Q6. What is MVT in Django? How is it different from MVC?**

> **MVT stands for Model-View-Template:**
> - **Model** — Defines database structure and business logic
> - **View** — Handles HTTP requests, fetches data, returns response
> - **Template** — HTML files with Django template language for display
>
> **vs MVC:** In traditional MVC, Controller handles routing. In Django, the URL
> dispatcher handles routing, so the "View" acts as the Controller, and "Template"
> acts as the View. Django calls it MVT instead of MVC.

---

**Q7. What is ORM? How did you use it?**

> ORM (Object Relational Mapper) allows you to interact with the database using Python
> objects instead of SQL queries. For example:
> ```python
> # Without ORM (SQL):
> SELECT * FROM bookings WHERE status = 'pending';
>
> # With Django ORM:
> Booking.objects.filter(status='pending')
> ```
> I used ORM throughout — for filtering bookings, updating stock, counting records, etc.

---

**Q8. Explain your database design / main models.**

> I have 6 main models:
> 1. **CustomUser** — Extends Django's AbstractUser, adds `role` field
> 2. **Category** — Equipment categories (Microcontroller, Sensor, etc.)
> 3. **Lab** — Physical labs (Lab A, B, C, D, E)
> 4. **Equipment** — Main inventory table with auto-generated asset ID and QR code
> 5. **Booking** — Booking requests with status lifecycle
> 6. **IssueLog** — Records physical issue event and condition on return
> 7. **Maintenance** — Tracks damaged/lost equipment until resolved

---

**Q9. How does QR code generation work in your project?**

> When a new equipment record is saved, the `save()` method triggers `_generate_qr_code()`.
> This function uses the Python `qrcode` library to create a QR image encoding the
> equipment's detail page URL. The image is saved in the `media/qr_codes/` folder.
> Staff can scan the QR with any phone camera to instantly view that equipment's details.

---

**Q10. How did you implement role-based access control?**

> I created a `@role_required` decorator in `accounts/decorators.py`. It checks
> `request.user.role` and redirects with an error message if the role doesn't match.
> Example:
> ```python
> @role_required('admin')
> def equipment_add(request):
>     # Only admin can access this
> ```
> The `CustomUser` model also has helper properties like `is_admin_user`,
> `can_manage_bookings`, and `can_request_booking` for use in templates.

---

**Q11. Explain the booking lifecycle.**

> The booking goes through 5 stages:
> 1. **Pending** — Student submits request
> 2. **Approved** — Staff verifies availability and approves
> 3. **Issued** — Equipment physically handed over; stock decreases
> 4. **Completed** — Equipment returned (condition checked)
> 5. **Rejected** — Request denied (with reason)
>
> Each stage change is logged with who performed the action and when.

---

**Q12. How does stock management work automatically?**

> - When equipment is **issued** → `available_quantity` decreases by booked quantity
> - When returned **in good condition** → `available_quantity` increases back
> - When returned **damaged/lost** → a Maintenance record is created, stock is NOT restored
> - When maintenance is **resolved** → `Maintenance.resolve()` method restores stock
>
> This ensures the system always reflects the true physical availability.

---

**Q13. What is CSRF? How does Django handle it?**

> CSRF (Cross-Site Request Forgery) is an attack where a malicious site tricks a logged-in
> user's browser to submit unauthorized requests. Django handles it automatically:
> - Every form includes `{% csrf_token %}` — a hidden field with a secret token
> - Django validates this token on every POST request
> - If the token is missing or wrong, the request is rejected with a 403 error

---

**Q14. What is a Migration in Django?**

> Migrations are Django's way of propagating model changes to the database. When I modify
> a model (add a field, change a relationship), I run:
> ```
> python manage.py makemigrations  # Creates migration file
> python manage.py migrate         # Applies changes to DB
> ```
> It's like version control for the database schema.

---

**Q15. How did you create the charts in the dashboard?**

> I used **Chart.js** (JavaScript library). In the Django view, I prepare data using
> ORM queries and convert it to JSON using Python's `json.dumps()`. This JSON is passed
> to the template as a context variable. In the template, Chart.js reads this data and
> renders:
> - **Doughnut chart** — Equipment count by category
> - **Line chart** — Monthly bookings (last 6 months)
> - **Bar chart** — Top 5 most booked equipment

---

## SECTION 3: Design Questions

**Q16. What is an ER Diagram? Explain your project's ER diagram.**

> ER (Entity-Relationship) Diagram shows entities (tables) and their relationships.
> In my project:
> - A `CustomUser` can make many `Booking` records (1-to-Many)
> - An `Equipment` can appear in many `Booking` records (1-to-Many)
> - Each `Booking` has one `IssueLog` (1-to-1)
> - An `IssueLog` may trigger one `Maintenance` record (1-to-0/1)
> - `Equipment` belongs to one `Category` and one `Lab`

---

**Q17. What is a DFD? Explain Level 0 and Level 1.**

> **DFD (Data Flow Diagram)** shows how data moves through the system.
> - **Level 0 (Context):** Shows the entire system as one box with external actors
>   (Users input data → System processes → Database stores → Reports output)
> - **Level 1:** Breaks the system into 6 main processes:
>   1. Authentication
>   2. Equipment Lookup
>   3. Booking Management
>   4. Stock Update
>   5. Maintenance Tracking
>   6. Reporting

---

**Q18. What design pattern does your project follow?**

> The project follows **MVT (Model-View-Template)** pattern — a variant of MVC.
> It also implements:
> - **Decorator pattern** — `@role_required` and `@login_required_custom`
> - **Repository pattern** — ORM abstracts all DB operations
> - **Factory pattern** — Auto-generation of asset IDs and booking references

---

## SECTION 4: Problem-Solving Questions

**Q19. What challenges did you face and how did you solve them?**

> 1. **Stock inconsistency bug:** When multiple bookings were approved simultaneously,
>    stock could go negative. Fixed by re-checking availability at issue time (not just approval).
>
> 2. **QR code on Windows:** Image generation path issues. Fixed by using
>    `os.path.join()` for cross-platform paths.
>
> 3. **Session after password change:** User was logged out after changing password.
>    Fixed using Django's `update_session_auth_hash()` to maintain session.
>
> 4. **Role confusion in templates:** Used custom model properties
>    (`can_manage_bookings`) instead of string comparisons for cleaner template logic.

---

**Q20. If you had more time, what would you add?**

> 1. **Email notifications** — Auto-email when booking is approved/rejected
> 2. **Mobile QR scanner** — Camera-based QR scan on smartphone
> 3. **Fine system** — Auto-calculate penalties for overdue returns
> 4. **REST API** — So the system can integrate with college ERP
> 5. **Calendar view** — Visual booking calendar per equipment item

---

## SECTION 5: Quick-Fire Questions

| Question | Answer |
|----------|--------|
| Full form of ORM? | Object Relational Mapper |
| Full form of CRUD? | Create, Read, Update, Delete |
| Full form of MVT? | Model, View, Template |
| What port does Django run on? | 8000 (default) |
| What port does MySQL run on? | 3306 (default) |
| What command creates superuser? | `python manage.py createsuperuser` |
| What command runs migrations? | `python manage.py migrate` |
| What command applies model changes? | `python manage.py makemigrations` |
| What is `settings.py`? | Django configuration file |
| What is `urls.py`? | URL routing configuration |
| What is `requirements.txt`? | List of Python dependencies |
| What command installs requirements? | `pip install -r requirements.txt` |
| What is a virtual environment? | Isolated Python environment for project |
| What is Bootstrap? | CSS framework for responsive design |
| What is Chart.js? | JavaScript library for data charts |
| What is CSRF? | Cross-Site Request Forgery protection |
| How many user roles? | 4 (Admin, Staff, Faculty, Student) |
| How many business rules? | 9 |
| How many test cases passed? | 20/20 |
| What generates QR codes? | Python `qrcode` library |

---

*Best of luck for your viva! You've built something real — be confident!* 🎓
