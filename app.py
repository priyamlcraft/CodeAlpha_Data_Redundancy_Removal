import streamlit as st
import pandas as pd
import sqlite3
import re
from datetime import datetime

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Data Redundancy Removal System",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_NAME = "redundancy_database.db"


# ================= CUSTOM CSS =================

st.markdown("""
<style>

/* Main background */
.stApp {
    background:
        linear-gradient(
            120deg,
            rgba(9, 12, 42, 0.94),
            rgba(36, 22, 88, 0.88),
            rgba(12, 35, 78, 0.92)
        ),
        url("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=2000&q=85");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* General text */
h1, h2, h3, h4, p, label {
    color: #ffffff !important;
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #ffffff;
    padding: 20px 10px 5px 10px;
    text-shadow: 0 0 18px rgba(130, 100, 255, 0.7);
}

.subtitle {
    text-align: center;
    color: #d8d8ff !important;
    font-size: 16px;
    margin-bottom: 30px;
}

/* Glass cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.09);
    border: 1px solid rgba(255, 255, 255, 0.20);
    border-radius: 18px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.20);
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(190, 170, 255, 0.30);
    padding: 18px;
    border-radius: 16px;
}

div[data-testid="stMetricLabel"] {
    color: #dedaff !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 800;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #536dfe, #9b59f6);
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #7655ff, #bd62ff);
    box-shadow: 0 0 18px rgba(150, 100, 255, 0.55);
    transform: translateY(-2px);
}

/* Input fields */
div[data-baseweb="input"] input,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] textarea {
    background: rgba(255, 255, 255, 0.95) !important;
    color: #17172c !important;
    border-radius: 9px !important;
}

/* File uploader */
div[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.08);
    border: 1px dashed #a99aff;
    border-radius: 14px;
    padding: 15px;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
}

/* Section headings */
.section-heading {
    color: #d7caff;
    font-size: 23px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #d4d0f5;
    padding: 25px 5px;
    font-size: 13px;
}

hr {
    border-color: rgba(255,255,255,0.20);
}

</style>
""", unsafe_allow_html=True)


# ================= DATABASE =================

def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


create_table()


# ================= VALIDATION =================

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))


# ================= ADD RECORD =================

def add_record(name, email, phone):

    name = str(name).strip()
    email = str(email).strip().lower()
    phone = str(phone).strip()

    if not name or not email:
        return "empty"

    if not validate_email(email):
        return "invalid_email"

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO records
            (name, email, phone, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            email,
            phone,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        return "success"

    except sqlite3.IntegrityError:
        return "duplicate"

    except sqlite3.Error:
        return "error"

    finally:
        conn.close()


# ================= GET RECORDS =================

def get_records():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM records ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


# ================= CSV CLEANING =================

def clean_dataframe(df):

    df.columns = df.columns.str.strip().str.lower()

    required_columns = ["name", "email", "phone"]

    if not all(col in df.columns for col in required_columns):
        return None, 0, 0

    df = df[required_columns].copy()

    df["name"] = df["name"].fillna("").astype(str).str.strip()
    df["email"] = (
        df["email"].fillna("").astype(str).str.strip().str.lower()
    )
    df["phone"] = df["phone"].fillna("").astype(str).str.strip()

    original_count = len(df)

    df = df[
        (df["name"] != "") &
        (df["email"] != "") &
        (df["email"].apply(validate_email))
    ].copy()

    invalid_count = original_count - len(df)

    before = len(df)

    df = df.drop_duplicates(
        subset=["email"],
        keep="first"
    )

    duplicate_count = before - len(df)

    return df, duplicate_count, invalid_count


# ================= CSV IMPORT =================

def save_csv_records(df):

    conn = get_connection()
    cursor = conn.cursor()

    added = 0
    existing = 0

    try:

        for _, row in df.iterrows():

            try:
                cursor.execute("""
                    INSERT INTO records
                    (name, email, phone, created_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    row["name"],
                    row["email"],
                    row["phone"],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))

                added += 1

            except sqlite3.IntegrityError:
                existing += 1

        conn.commit()

    finally:
        conn.close()

    return added, existing


# ================= DELETE RECORD =================

def delete_record(record_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM records WHERE id = ?",
        (record_id,)
    )

    conn.commit()
    conn.close()


# ================= HEADER =================

st.markdown("""
<div class="main-title">
    💠 DATA REDUNDANCY REMOVAL SYSTEM
</div>

<div class="subtitle">
    Smart Database Management | Duplicate Detection |
    Data Validation
</div>
""", unsafe_allow_html=True)


# ================= NOTIFICATIONS =================

if st.session_state.get("success_message"):
    st.success(st.session_state["success_message"])
    del st.session_state["success_message"]

if st.session_state.get("csv_result"):
    result = st.session_state["csv_result"]

    st.success("CSV processing completed!")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("CSV Duplicates Removed", result["duplicates"])
    col2.metric("New Records Added", result["added"])
    col3.metric("Existing Records Skipped", result["existing"])
    col4.metric("Invalid Rows", result["invalid"])

    del st.session_state["csv_result"]


# ================= DASHBOARD =================

records_df = get_records()

total_records = len(records_df)

unique_records = (
    records_df["email"].nunique()
    if not records_df.empty else 0
)

st.markdown(
    '<div class="section-heading">📊 Dashboard Overview</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Unique Records", unique_records)

with c2:
    st.metric("Total Database Records", total_records)

with c3:
    st.metric("Database Status", "Connected")


st.divider()


# ================= ADD NEW RECORD =================

st.markdown(
    '<div class="section-heading">➕ Add New Record</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    with st.form("record_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Full Name",
                placeholder="Enter full name"
            )

        with col2:
            email = st.text_input(
                "Email Address",
                placeholder="example@gmail.com"
            )

        phone = st.text_input(
            "Phone Number",
            placeholder="Enter phone number"
        )

        submitted = st.form_submit_button(
            "💾 Save Record",
            use_container_width=True
        )

        if submitted:

            result = add_record(name, email, phone)

            if result == "success":

                st.session_state["success_message"] = (
                    "Record saved successfully!"
                )

                st.rerun()

            elif result == "duplicate":

                st.warning(
                    "Duplicate detected! This email already exists."
                )

            elif result == "invalid_email":

                st.error("Please enter a valid email address.")

            elif result == "empty":

                st.error("Name and Email are required.")

            else:

                st.error("Something went wrong. Please try again.")


st.divider()


# ================= CSV UPLOAD =================

st.markdown(
    '<div class="section-heading">📁 Upload CSV File</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.write(
        "Upload your CSV file to automatically identify "
        "and remove duplicate records."
    )

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"],
        key="csv_upload"
    )

    if uploaded_file is not None:

        try:

            uploaded_df = pd.read_csv(uploaded_file)

            st.subheader("Uploaded Data Preview")

            st.dataframe(
                uploaded_df,
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                "✨ Remove Duplicates and Import",
                use_container_width=True
            ):

                cleaned_df, duplicates, invalid = clean_dataframe(
                    uploaded_df
                )

                if cleaned_df is None:

                    st.error(
                        "CSV must contain name, email, and phone columns."
                    )

                elif cleaned_df.empty:

                    st.warning(
                        "No valid records found in the CSV file."
                    )

                else:

                    added, existing = save_csv_records(cleaned_df)

                    st.session_state["csv_result"] = {
                        "duplicates": duplicates,
                        "added": added,
                        "existing": existing,
                        "invalid": invalid
                    }

                    st.rerun()

        except Exception as e:

            st.error(f"Unable to process CSV file: {e}")


st.divider()


# ================= DATABASE RECORDS =================

st.markdown(
    '<div class="section-heading">📋 Database Records</div>',
    unsafe_allow_html=True
)

records_df = get_records()

with st.container(border=True):

    if not records_df.empty:

        st.dataframe(
            records_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = records_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Database Records",
            data=csv_data,
            file_name="cleaned_database_records.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader("🗑️ Delete a Record")

        record_ids = records_df["id"].tolist()

        selected_id = st.selectbox(
            "Select Record ID",
            record_ids
        )

        if st.button(
            "Delete Selected Record",
            use_container_width=True
        ):

            delete_record(selected_id)

            st.session_state["success_message"] = (
                "Record deleted successfully!"
            )

            st.rerun()

    else:

        st.info(
            "No records found. Add a new record to get started."
        )


# ================= FOOTER =================

st.divider()

st.markdown("""
<div class="footer">
    <b>DATA REDUNDANCY REMOVAL SYSTEM</b><br>
    Developed using Python | Streamlit | Pandas | SQLite<br>
    CodeAlpha Cloud Computing Internship
</div>
""", unsafe_allow_html=True)
