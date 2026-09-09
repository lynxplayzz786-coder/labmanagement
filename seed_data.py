"""
Seed script — adds initial demo data to the database.
Run with: python manage.py shell < seed_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab_management.settings')
django.setup()

from accounts.models import CustomUser
from equipment.models import Category, Lab, Equipment

print("=" * 50)
print("Seeding database...")
print("=" * 50)

# ── Categories ────────────────────────────────────
categories_data = [
    {"name": "Microcontroller",  "description": "Arduino, Raspberry Pi, ESP32 etc."},
    {"name": "Oscilloscope",     "description": "Digital and analog oscilloscopes"},
    {"name": "Multimeter",       "description": "Digital multimeters for voltage/current measurement"},
    {"name": "Networking",       "description": "Routers, switches, cables, patch panels"},
    {"name": "Projector",        "description": "LCD/LED projectors for presentations"},
    {"name": "Sensor",           "description": "Temperature, humidity, IR, ultrasonic sensors"},
    {"name": "Cable",            "description": "USB, HDMI, Ethernet, power cables"},
]

categories = {}
for data in categories_data:
    cat, created = Category.objects.get_or_create(name=data["name"], defaults=data)
    categories[data["name"]] = cat
    print(f"  {'Created' if created else 'Exists '} Category: {data['name']}")

# ── Labs ──────────────────────────────────────────
labs_data = [
    {"name": "IoT Lab",           "location": "Block B, Room 101", "capacity": 30},
    {"name": "Computer Lab 1",    "location": "Block A, Room 201", "capacity": 40},
    {"name": "Computer Lab 2",    "location": "Block A, Room 202", "capacity": 40},
    {"name": "Electronics Lab",   "location": "Block C, Room 105", "capacity": 25},
    {"name": "Networking Lab",    "location": "Block B, Room 205", "capacity": 20},
]

labs = {}
for data in labs_data:
    lab, created = Lab.objects.get_or_create(name=data["name"], defaults=data)
    labs[data["name"]] = lab
    print(f"  {'Created' if created else 'Exists '} Lab: {data['name']}")

# ── Equipment ─────────────────────────────────────
equipment_data = [
    {
        "name": "Arduino Uno",
        "category": "Microcontroller",
        "lab": "IoT Lab",
        "quantity": 20,
        "available_quantity": 18,
        "description": "Arduino Uno R3 microcontroller board",
    },
    {
        "name": "Arduino Mega 2560",
        "category": "Microcontroller",
        "lab": "IoT Lab",
        "quantity": 10,
        "available_quantity": 10,
        "description": "Arduino Mega 2560 with 54 digital I/O pins",
    },
    {
        "name": "Raspberry Pi 4 Model B",
        "category": "Microcontroller",
        "lab": "IoT Lab",
        "quantity": 15,
        "available_quantity": 12,
        "description": "Raspberry Pi 4 Model B — 4GB RAM",
    },
    {
        "name": "Digital Oscilloscope",
        "category": "Oscilloscope",
        "lab": "Electronics Lab",
        "quantity": 8,
        "available_quantity": 6,
        "description": "100MHz digital oscilloscope with USB output",
    },
    {
        "name": "Digital Multimeter",
        "category": "Multimeter",
        "lab": "Electronics Lab",
        "quantity": 25,
        "available_quantity": 20,
        "description": "Auto-ranging digital multimeter",
    },
    {
        "name": "Managed Network Switch (24-port)",
        "category": "Networking",
        "lab": "Networking Lab",
        "quantity": 5,
        "available_quantity": 5,
        "description": "24-port Gigabit managed switch",
    },
    {
        "name": "Ethernet Patch Cable (Cat6)",
        "category": "Cable",
        "lab": "Networking Lab",
        "quantity": 100,
        "available_quantity": 85,
        "description": "Cat6 Ethernet patch cables — 1.5m, 3m",
    },
    {
        "name": "LCD Projector",
        "category": "Projector",
        "lab": "Computer Lab 1",
        "quantity": 3,
        "available_quantity": 3,
        "description": "1080p LCD projector — 3500 lumens",
    },
    {
        "name": "DHT22 Temperature & Humidity Sensor",
        "category": "Sensor",
        "lab": "IoT Lab",
        "quantity": 50,
        "available_quantity": 45,
        "description": "High-accuracy temp & humidity sensor",
    },
    {
        "name": "Ultrasonic Sensor (HC-SR04)",
        "category": "Sensor",
        "lab": "IoT Lab",
        "quantity": 40,
        "available_quantity": 38,
        "description": "HC-SR04 ultrasonic distance sensor",
    },
]

for data in equipment_data:
    cat = categories[data.pop("category")]
    lab = labs[data.pop("lab")]
    eq, created = Equipment.objects.get_or_create(
        name=data["name"],
        defaults={**data, "category": cat, "lab": lab}
    )
    print(f"  {'Created' if created else 'Exists '} Equipment: {eq.asset_id} — {eq.name}")

# ── Sample Users ──────────────────────────────────
users_data = [
    {"username": "staff1",   "email": "staff1@lab.com",   "role": "staff",   "first_name": "Ravi",    "last_name": "Kumar",   "password": "staff123"},
    {"username": "student1", "email": "s1@lab.com",       "role": "student", "first_name": "Rahul",   "last_name": "Sharma",  "password": "student123", "enrollment_no": "BCA2024001"},
    {"username": "student2", "email": "s2@lab.com",       "role": "student", "first_name": "Priya",   "last_name": "Verma",   "password": "student123", "enrollment_no": "BCA2024002"},
    {"username": "faculty1", "email": "f1@lab.com",       "role": "faculty", "first_name": "Dr. Anu", "last_name": "Singh",   "password": "faculty123"},
]

for data in users_data:
    password = data.pop("password")
    user, created = CustomUser.objects.get_or_create(
        username=data["username"],
        defaults=data
    )
    if created:
        user.set_password(password)
        user.save()
    print(f"  {'Created' if created else 'Exists '} User: {user.username} ({user.role})")

print()
print("=" * 50)
print("Seed complete!")
print()
print("Login credentials:")
print("  Admin:   admin / abhishek123")
print("  Staff:   staff1 / staff123")
print("  Faculty: faculty1 / faculty123")
print("  Student: student1 / student123")
print("=" * 50)
