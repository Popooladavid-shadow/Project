import streamlit as st
import sqlite3
import hashlib
from datetime import date

# ---------- DATABASE FUNCTIONS ----------
def create_usertable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def create_transaction_table():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_email TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    date TEXT,
                    status TEXT
                )''')
    conn.commit()
    conn.close()

def add_user(name, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
    conn.commit()
    conn.close()

def login_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    data = c.fetchone()
    conn.close()
    return data

def add_transaction(user_email, amount, description, date, status):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (user_email, amount, description, date, status) VALUES (?, ?, ?, ?, ?)',
              (user_email, amount, description, date, status))
    conn.commit()
    conn.close()

def get_transactions(user_email):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('SELECT date, amount, description, status FROM transactions WHERE user_email = ?', (user_email,))
    data = c.fetchall()
    conn.close()
    return data

# ---------- PASSWORD SECURITY ----------
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed):
    if make_hashes(password) == hashed:
        return hashed
    return False

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="POS Login System", page_icon="💳", layout="centered")

# ---------- STYLE ----------
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    }
    .main {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #ff4b4b;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        padding: 0.6em 1.5em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff7b7b;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- CREATE TABLES ----------
create_usertable()
create_transaction_table()

# ---------- APP TITLE ----------
st.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/Logo_placeholder.png", width=120)
st.title("💳 POS Transaction System")

menu = ["Home", "Login", "Sign Up"]
choice = st.sidebar.selectbox("Navigation", menu)

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------- HOME ----------
if choice == "Home":
    st.markdown("### 👋 Welcome to the POS Transaction System")
    st.markdown("""
    This system allows you to:
    - 🔐 Create secure accounts  
    - 💼 Log in to record transactions  
    - 🧾 View all your data safely  
    """)
    st.info("Use the sidebar to **Sign Up** or **Login** to continue.")

# ---------- SIGN UP ----------
elif choice == "Sign Up":
    st.subheader("Create a New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if name and email and password:
            hashed_pass = make_hashes(password)
            try:
                add_user(name, email, hashed_pass)
                st.success("🎉 Account created successfully! You can now log in.")
            except sqlite3.IntegrityError:
                st.error("⚠️ This email is already registered.")
        else:
            st.warning("Please fill in all fields.")

# ---------- LOGIN ----------
elif choice == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed_pass = make_hashes(password)
        result = login_user(email, hashed_pass)

        if result:
            st.session_state.logged_in = True
            st.session_state.user_name = result[1]
            st.session_state.user_email = result[2]
            st.success(f"Welcome back, {result[1]}!")
        else:
            st.error("Invalid email or password.")

# ---------- DASHBOARD ----------
if st.session_state.logged_in:
    st.success(f"✅ Logged in as {st.session_state.user_name}")
    st.markdown("---")

    st.subheader("💰 Record a New Transaction")

    with st.form("transaction_form"):
        amount = st.number_input("Amount (₦)", min_value=0.0, step=100.0)
        description = st.text_input("Description")
        t_date = st.date_input("Date", value=date.today())
        status = st.selectbox("Status", ["Success", "Failed"])
        submit = st.form_submit_button("Save Transaction")

        if submit:
            if amount > 0 and description:
                add_transaction(st.session_state.user_email, amount, description, str(t_date), status)
                st.success("✅ Transaction saved successfully!")
            else:
                st.warning("Please fill in all fields before saving.")

    st.markdown("---")
    st.subheader("📜 Your Transactions")
    data = get_transactions(st.session_state.user_email)

    if data:
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No transactions yet. Add one above!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.info("You have logged out successfully.")
