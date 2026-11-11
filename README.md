# Data Redundancy Removal System

### Smart Database Management | Duplicate Detection | Data Validation

A database management application developed using Python, Streamlit, and SQLite to identify duplicate records, validate user information, and maintain a clean and organized database.

This project helps prevent duplicate entries, manage records efficiently, and ensure data consistency through an interactive web-based dashboard.

## Features

- **Interactive Dashboard:** Displays total unique records, total database records, and database connection status.
- **Add New Records:** Allows users to add records with name, email, and phone number.
- **Duplicate Detection:** Prevents duplicate entries using unique email validation.
- **Data Validation:** Checks user input to maintain valid records.
- **CSV Upload:** Supports uploading CSV files for bulk data import.
- **Duplicate Removal:** Identifies and removes duplicate entries from uploaded CSV data.
- **Database Management:** Stores and manages records using SQLite.
- **Delete Records:** Allows users to select and delete existing records.
- **CSV Export:** Enables downloading database records as a CSV file.
- **User-Friendly Interface:** Includes a modern blue-purple gradient design with an interactive dashboard.

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- CSV

## Project Structure

```text
CodeAlpha_Data_Redundancy_Removal/
│
├── app.py
├── requirements.txt
├── README.md
└── redundancy_database.db
```

**Note:** The SQLite database file is automatically created when the application runs for the first time.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/priyamlcraft/CodeAlpha_Data_Redundancy_Removal.git
```

### 2. Navigate to the Project Folder

```bash
cd CodeAlpha_Data_Redundancy_Removal
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser.

## How to Use

1. Launch the application using Streamlit.
2. View the dashboard to check database statistics.
3. Enter a name, email, and phone number to add a new record.
4. Upload a CSV file to import multiple records.
5. Use the duplicate removal feature to prevent repeated entries.
6. View all stored records in the database section.
7. Select a record to delete it when required.
8. Download the database records in CSV format.

## Database Management

The application uses SQLite to store records locally.

Each record contains:
- Unique ID
- Name
- Email
- Phone Number
- Created Date and Time

The email field is configured with a UNIQUE constraint to prevent duplicate email entries in the database.

## Learning Outcomes

Through this project, I gained practical experience in:

- Python application development
- Database connectivity and SQLite operations
- Data validation and duplicate detection
- CSV file processing using Pandas
- Building interactive applications with Streamlit
- Database record management and data consistency

## Internship Information

**Internship:** Cloud Computing Internship  
**Organization:** CodeAlpha  
**Project:** Task 1 – Data Redundancy Removal System

---

**Developed as part of the CodeAlpha Cloud Computing Internship.**
