# 🏥 TeleMedLink – Telemedicine Care Platform

**TeleMedLink** is a comprehensive telemedicine platform designed to bridge the gap between patients and healthcare providers. It facilitates remote consultations, intelligent diagnostics, appointment scheduling, data visualization, and more — all in one intuitive web system.

## 🚀 Features

### 👨‍⚕️ For Doctors:
- View and manage patient appointments
- Accept, cancel (with comments),
- View appointment insights via interactive graphs
- Download appointment summaries in PDF format
- View and manage documents related to consultations

### 🧑‍💻 For Patients:
- Register, log in, and book appointments with available doctors
- Track upcoming and past appointments with filtering
- View appointment statistics in charts
- Download appointment history in PDF
- Password reset functionality

### 🛠 Admin Panel:
- Manage doctors and patients
- Monitor system analytics and logs

### 📈 Data Visualization:
- Monthly appointment trends
- Status-based summaries (Accepted, Cancelled, Pending)
- Dashboard charts for both patients and doctors

### 📂 Documents:
- Each user can access a "Documents" page to download appointments and summaries

---

## 💻 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Bootstrap, Chart.js
- **Database**: SQLite (Dev) / PostgreSQL (Production Ready)
- **Authentication**: Django Auth, Password Reset via Email
- **PDF Generation**: xhtml2pdf
- **Charting**: Chart.js for data visualization

---

## 📸 Screenshots

_Coming soon..._

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.12+
- pip
- Git

### Installation

```bash
git clone https://github.com/yourusername/TeleMedLink.git
cd TeleMedLink
python -m venv env
env\Scripts\activate   # On Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
