# project-1
Client Query Management System

# 💬 Client Query Management System

This is a Streamlit-based web application designed to manage client support queries efficiently. It provides two distinct dashboards: one for **Clients** to submit new queries, and one for **Support Staff** to view, track, and resolve open tickets.

## 🚀 Features

* **Role-Based Authentication:** Separate login for Client and Support roles.
* **Client Dashboard:** Form for submitting new support queries with contact details.
* **Support Dashboard:** Real-time view of all open queries and a form to mark queries as resolved (closed).
* **Database Integration:** Uses **PostgreSQL** to securely store user and query data.

## Technology Stack

* **Frontend/App Framework:** Streamlit
* **Backend/Database:** PostgreSQL
* **Python Libraries:** `psycopg2`, `pandas`, `hashlib`

---

## Setup and Installation

Follow these steps to set up the project locally:

### 1. Prerequisites

Before starting, ensure you have the following installed:

* **Python 3.8+**
* **PostgreSQL:** The database must be running, and you should have a user with the specified credentials.
  

### 2. Install Dependencies

Create a virtual environment (recommended) and install the necessary Python packages:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
