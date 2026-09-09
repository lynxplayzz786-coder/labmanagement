# TITLE OF THE PROJECT
**LAB EQUIPMENT RENTAL & MANAGEMENT SYSTEM**

**PROJECT SYNOPSIS REPORT**

**GULZAR GROUP OF INSTITUTIONS**  
*(Affiliated to IKG Punjab Technical University, Kapurthala)*

**Submitted by:**  
Abhishek (2433410)
Aditya Kumar (2433414)
Chhaya Chouhan (2433451)
Chahta Sinha (2433449)
Harjit Kaur (2433495)
Prince (2433601)

**Under the Guidance of:**  
Ms. Manisha Chawla  
(Designation / Supervisor)

**Department:** BCA  
**Year:** Final Year  
**Academic Session:** 2026 – 2027

---

## 2. Introduction & Background
The management of laboratory equipment is a critical operational task for educational institutions, especially in departments dealing with computers, electronics, and hardware tools. Historically, institutions have relied on manual, paper-based ledger systems to issue and receive equipment like microcontrollers, sensors, networking tools, and testing devices. While this method serves the basic purpose of recording transactions, it scales poorly as the inventory and student population grow. 

In the digital era, automating the tracking of physical assets is essential to prevent loss, ensure fair utilization, and hold borrowers accountable for damages. This project introduces the **Lab Equipment Rental & Management System (LabMS)**—a centralized, web-based platform designed specifically for the college ecosystem. It provides a structured, role-based approach (Admin, Staff, Faculty, Student) to digitize the entire lifecycle of equipment borrowing, from initial request to final return and maintenance. By incorporating technologies like QR code generation for quick asset identification and automated stock control algorithms, this system modernizes lab administration, ensuring that resources are utilized optimally and efficiently.

## 3. Problem Statement
Lab equipment management in most college computer and electronics labs currently suffers from a heavy reliance on manual paper registers. The core issues this project seeks to address include:
*   **Lack of Real-Time Visibility:** Students and faculty cannot check the availability of equipment without physically visiting the lab.
*   **Manual Record Errors:** Handwritten logs are error-prone, hard to read, and time-consuming to search, making it difficult to trace who borrowed what and when.
*   **Poor Accountability for Damages:** When equipment is returned damaged, it is rarely documented properly, and faulty equipment often gets re-issued to other students by mistake.
*   **Absence of Analytics:** Administrators have no statistical data on which equipment is most utilized, hindering smart procurement decisions.
*   **Access Control Gaps:** Lack of a formal approval hierarchy leads to unauthorized borrowing of expensive or scarce equipment.

## 4. Objectives
The primary objectives of this project are to:
1.  **Design and develop** a role-based web application to digitize lab equipment inventory and borrowing workflows.
2.  **Implement an automated stock management algorithm** that accurately tracks real-time availability based on booking approvals, issues, and returns.
3.  **Integrate QR code generation** for every physical asset to enable quick digital identification and lookup by lab staff.
4.  **Develop a condition-based return and maintenance tracking module** to ensure damaged equipment is isolated from available stock until resolved.
5.  **Create an analytical dashboard** providing real-time statistics and visual reports (Chart.js) on equipment utilization and booking statuses.

## 5. Scope of the Project

**5.1 In-Scope Features (Functional Scope)**
*   **Inventory & QR Management:** Add, edit, and categorize equipment across multiple physical labs. Automatic generation of unique Asset IDs and QR codes.
*   **Booking Lifecycle Workflow:** A 5-stage digital pipeline (Pending → Approved → Issued → Completed → Rejected) for handling student and faculty requests.
*   **Role-Based Access Control (RBAC):** Distinct dashboards and permissions for Admins (full control/reports), Staff (approvals/returns/maintenance), and Students/Faculty (browsing/requesting).
*   **Dynamic Stock Enforcement:** Business logic that prevents over-booking and automatically deducts/restores available quantities upon physical issue and return.
*   **Maintenance Module:** System to flag equipment returned as 'Damaged' or 'Lost', moving it to a maintenance queue where stock is frozen until an admin marks it as resolved.
*   **Visual Analytics & Reports:** Interactive pie, line, and bar charts for admins to monitor total bookings, category distribution, and top utilized equipment.

**5.2 Out-of-Scope (Exclusions)**
*   Integration with external SMS or WhatsApp gateways for notifications.
*   Developing native mobile applications for iOS or Android.
*   Financial penalty/payment gateway integration for lost equipment.
*   Enterprise-grade cloud deployment across multiple separate college campuses.

**Target Audience/Beneficiaries:** 
BCA/B.Tech students requiring lab hardware for projects, lab assistants/staff managing daily checkouts, and college administrators overseeing asset procurement and utilization.

## 6. Proposed Methodology

**Tools and Technologies:**
*   **Front-end:** HTML5, CSS3, Bootstrap 5.3, Chart.js (for analytics), Font Awesome Icons.
*   **Back-end:** Python 3.11, Django 4.2 LTS Framework (MVT Architecture).
*   **Database:** MySQL 8.0 (Relational Database Management).
*   **Additional Libraries:** `qrcode` (for QR generation), `Pillow` (for image processing).
*   **Dev Environment:** Visual Studio Code, virtualenv.

**Step-by-Step Approach (Activities):**
1.  **Requirement Analysis:** Identify pain points in the current manual register system through observation.
2.  **UI/UX Prototyping:** Design wireframes for dashboards, equipment catalogs, and staff approval panels.
3.  **Database Design:** Create relational schema (CustomUser, Equipment, Category, Lab, Booking, IssueLog, Maintenance) and ER diagrams.
4.  **Back-end Development:** Implement Django models, authentication, role-decorators, and the core booking lifecycle logic.
5.  **Front-end Development:** Build responsive Bootstrap templates and integrate them with Django views.
6.  **Feature Integration:** Implement QR code generation and Chart.js reporting.
7.  **Testing:** Perform unit and integration testing using sample data covering all business rules (e.g., booking exceeding stock, returning damaged goods).

## 7. Expected Outcomes

**Deliverables:**
*   A fully functional web-based prototype of the Lab Equipment Rental & Management System.
*   A comprehensive project report documenting system architecture, database schema, and test cases.
*   Sample database export containing dummy categories, equipment, and user roles for demonstration.

**Benefits to Academia:**
*   **For Students:** Saves time by allowing remote browsing and booking of available equipment.
*   **For Staff:** Drastically reduces paperwork and the physical effort required to track down missing items.
*   **For Administration:** Provides actionable data on hardware usage, helping optimize the budget for purchasing new lab equipment.

## 8. Resources Required

*   **Hardware:** Personal Computer / Laptop (Windows/macOS/Linux) with minimum 8GB RAM.
*   **Software:** Python 3.11, Django 4.2, MySQL Server 8.0, Visual Studio Code, Web Browser (Chrome/Firefox).
*   **Lab Facilities:** Institutional computer lab for local network testing and presentation.
*   **Datasets:** Dummy data for categories, labs, and equipment for system functional testing.
*   **External Support:** Project Supervisor (Ms. Manisha Chawla) for architectural guidance and validation.

## 9. 15-Week Progress Plan (Tabular)

| Week | Phase | Tasks / Description |
| :--- | :--- | :--- |
| **Week 1-2** | Research | Requirement gathering, literature review, and problem finalization. |
| **Week 3-4** | Research | Objective framing, methodology design, and UI/UX wireframing. |
| **Week 5-6** | Setup | Database schema design, Django models creation, and tool setup. |
| **Week 7-8** | Setup | Custom Authentication, RBAC integration. *(Mid Review & Progress Report)* |
| **Week 9-11** | Execution | Development of Equipment Catalog, QR codes, Booking workflows, and Staff panels. |
| **Week 12-13** | Execution | Integration of Chart.js Dashboards, Bug fixing, and edge-case testing. |
| **Week 14** | Completion | Draft project documentation and report preparation. |
| **Week 15** | Completion | Final project review, formatting, and preparation for final presentation/submission. |

## 10. Gantt Chart / Visual Timeline
*(Please insert the screenshot of the HTML Gantt chart here)*

## 11. Conclusion
The "Lab Equipment Rental & Management System" represents a significant leap forward in academic asset management. By transitioning from error-prone manual paper registers to a centralized, QR-enabled web platform, this system provides unmatched accountability, security, and convenience. Furthermore, this project directly contributes to the Sustainable Development Goal (SDG) 12 (Responsible Consumption and Production) by optimizing the usage of electronic components, preventing equipment loss, and enabling better tracking of maintenance to reduce e-waste in the institution.

## 12. References

1.  Django Software Foundation. (2023). *Django Documentation v4.2*. Retrieved from https://docs.djangoproject.com/en/4.2/
2.  Oracle. (2023). *MySQL 8.0 Reference Manual*. Retrieved from https://dev.mysql.com/doc/refman/8.0/en/
3.  Bootstrap Core Team. (2023). *Bootstrap 5.3 Official Documentation*. Retrieved from https://getbootstrap.com/docs/5.3/
4.  Chart.js Contributors. (2023). *Chart.js Documentation v4.4*. Retrieved from https://www.chartjs.org/docs/
5.  Singh, R., & Kumar, A. (2019). Digital Inventory Management in Educational Institutions. *International Journal of Computer Applications*, 178(32), 12-17.
6.  Kumar, V., & Patel, S. (2021). QR Code Based Asset Management System in Academic Labs. *Journal of Engineering and Technology*, 12(4), 55-62.
7.  Greenfeld, D. R., & Roy, A. (2022). *Two Scoops of Django 3.x: Best Practices for the Django Web Framework*. Two Scoops Press.
8.  Yadav, R., & Sharma, N. (2020). Digital token-based tracking system for university assets. *International Journal of Engineering Research & Technology*, 9(6).
9.  Duckett, J. (2014). *HTML and CSS: Design and Build Websites*. John Wiley & Sons.
10. Kaur, H., & Singh, A. (2021). Role of Python-MySQL based web applications in small-scale digitalization. *Journal of Emerging Technologies and Innovative Research*, 8(3).
