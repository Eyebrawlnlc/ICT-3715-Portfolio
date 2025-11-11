# locker_gui_mysql.py
from datetime import date
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk

# -------------------------
# Database connection info
# -------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Bat2-3man",
    "database": "amandla_locker_system",
    "auth_plugin": "mysql_native_password"  # optional depending on your MySQL setup
}

def db_connect():
    """Return a new MySQL connection (caller should close)."""
    return mysql.connector.connect(**DB_CONFIG)

# -------------------------
# Utility functions
# -------------------------
def simulate_email(to_email, subject, body):
    """Simulate sending an email by showing a popup."""
    messagebox.showinfo("Simulated Email",
                        f"To: {to_email}\nSubject: {subject}\n\n{body}")

def fetchone(query, params=()):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def fetchall(query, params=()):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def execute(query, params=()):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    lastrowid = cur.lastrowid
    cur.close()
    conn.close()
    return lastrowid

# -------------------------
# Login and main window
# -------------------------
root = tk.Tk()
root.title("Amandla High School Locker System Login")
root.geometry("420x360")
root.resizable(False, False)

frame = tk.Frame(root, padx=15, pady=15)
frame.pack(expand=True, fill="both")

title = tk.Label(frame, text="Locker Booking System - Login", font=("Helvetica", 14, "bold"))
title.pack(pady=(0,10))

tk.Label(frame, text="Email:").pack(anchor="w")
email_entry = tk.Entry(frame, width=40)
email_entry.pack(pady=3)

tk.Label(frame, text="Password:").pack(anchor="w")
password_entry = tk.Entry(frame, width=40, show="*")
password_entry.pack(pady=3)

tk.Label(frame, text="Login as:").pack(anchor="w")
role_var = tk.StringVar(value="Parent")
role_combo = ttk.Combobox(frame, textvariable=role_var, values=["Parent", "Administrator"], state="readonly", width=37)
role_combo.pack(pady=5)

info_label = tk.Label(frame, text="Admin: admin@amandla.local / admin123\nParent accounts use parent email; default password = parentpass", font=("Helvetica", 8), fg="gray")
info_label.pack(pady=(6,8))

# -------------------------
# Parent Dashboard
# -------------------------
def open_parent_dashboard(parent_email):
    # fetch parent record
    pr = fetchone("SELECT parent_id, first_name, last_name FROM parents WHERE email = %s", (parent_email,))
    if not pr:
        messagebox.showerror("Error", "Parent account not found in database.")
        return
    parent_id, first_name, last_name = pr
    parent_name = f"{first_name} {last_name}"

    pwin = tk.Toplevel(root)
    pwin.title("Parent Dashboard - Locker Booking")
    pwin.geometry("760x520")

    tk.Label(pwin, text=f"Parent Dashboard — {parent_name}", font=("Helvetica", 13, "bold")).pack(pady=8)
    tk.Label(pwin, text="Your Students:", font=("Helvetica", 11, "underline")).pack(anchor="w", padx=10)

    # Student Treeview
    cols = ("StudentID", "First Name", "Last Name", "Grade", "Locker", "Application Status", "Payment")
    tree = ttk.Treeview(pwin, columns=cols, show="headings", height=8)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=110 if col != "Locker" else 80)
    tree.pack(padx=10, pady=(4,8))

    def refresh_parent_students():
        for i in tree.get_children():
            tree.delete(i)
        # For each student of this parent get locker info and booking/payment
        rows = fetchall('''
            SELECT s.student_id, s.first_name, s.last_name, s.grade,
                   l.locker_number,
                   CASE WHEN b.locker_id IS NULL THEN 'Waitlisted' ELSE 'Booked' END AS app_status,
                   COALESCE(b.payment_status, 'Unpaid')
            FROM students s
            LEFT JOIN bookings b ON s.student_id = b.student_id
            LEFT JOIN lockers l ON b.locker_id = l.locker_id
            WHERE s.parent_id = %s
            ORDER BY s.student_id
        ''', (parent_id,))
        for r in rows:
            tree.insert("", "end", values=r)

    refresh_parent_students()

    # Locker selection area
    tk.Label(pwin, text="Available Lockers:").pack(anchor="w", padx=10)
    locker_combo = ttk.Combobox(pwin, values=[], width=18)
    locker_combo.pack(padx=10, pady=6, anchor="w")

    def refresh_lockers():
        lockers = fetchall("SELECT locker_id, locker_number FROM lockers WHERE status='Available' ORDER BY locker_number")
        locker_map = {str(l[1]): l[0] for l in lockers}
        locker_combo['values'] = list(locker_map.keys())
        locker_combo._map = locker_map  # attach map for later use

    refresh_lockers()

    # Student selection combobox for applying
    tk.Label(pwin, text="Select Student to apply for locker:").pack(anchor="w", padx=10)
    student_combo = ttk.Combobox(pwin, values=[], width=40)
    student_combo.pack(padx=10, pady=6, anchor="w")

    def refresh_student_combo():
        rows = fetchall("SELECT student_id, first_name, last_name, grade FROM students WHERE parent_id=%s", (parent_id,))
        student_combo_vals = [f"{r[1]} {r[2]} (ID {r[0]}) - {r[3]}" for r in rows]
        student_combo['values'] = student_combo_vals
        student_combo._ids = {val: r[0] for val, r in zip(student_combo_vals, rows)}  # map to id

    refresh_student_combo()

    # Application outcome display function
    def check_application_outcome():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a student row to check outcome.")
            return
        item = tree.item(sel[0])['values']
        student_id = item[0]
        # find latest booking for this student
        booking = fetchone("SELECT booking_id, locker_id, booking_date FROM bookings WHERE student_id=%s ORDER BY booking_id DESC LIMIT 1", (student_id,))
        if not booking:
            messagebox.showinfo("Outcome", "No application found for this student.")
            return
        booking_id, locker_id, booking_date = booking
        if locker_id is None:
            messagebox.showinfo("Outcome", f"Status: Waitlisted\nBooking ID: {booking_id}\nApplied on: {booking_date}")
        else:
            locker = fetchone("SELECT locker_number FROM lockers WHERE locker_id=%s", (locker_id,))
            locker_no = locker[0] if locker else str(locker_id)
            messagebox.showinfo("Outcome", f"Status: Booked\nLocker: {locker_no}\nBooking ID: {booking_id}\nBooked on: {booking_date}")

    # Apply for locker
    def apply_for_locker():
        sel_student = student_combo.get()
        if not sel_student:
            messagebox.showerror("Missing", "Select a student to apply for.")
            return
        # parse student id
        if "(ID " not in sel_student:
            messagebox.showerror("Error", "Invalid student selection.")
            return
        sid = int(sel_student.split("(ID ")[1].split(")")[0])
        # Check if student already has a booking
        existing = fetchone("SELECT booking_id, locker_id FROM bookings WHERE student_id=%s ORDER BY booking_id DESC LIMIT 1", (sid,))
        if existing:
            bid, lid = existing
            if lid is not None:
                messagebox.showinfo("Already Booked", "This student already has a booked locker.")
                return
            else:
                # already waitlisted
                messagebox.showinfo("Already Applied", "This student is already on the waiting list.")
                return
        # Check available lockers
        available = fetchall("SELECT locker_id, locker_number FROM lockers WHERE status='Available' ORDER BY locker_number LIMIT 1")
        if available:
            # assign the first available locker immediately
            locker_id, locker_number = available[0]
            # create booking with locker_id
            execute("INSERT INTO bookings (parent_id, student_id, locker_id, booking_date, payment_status) VALUES (%s,%s,%s,%s,%s)",
                    (parent_id, sid, locker_id, date.today().isoformat(), "Unpaid"))
            # update locker status to Booked
            execute("UPDATE lockers SET status='Booked' WHERE locker_id=%s", (locker_id,))
            # notify parent
            simulate_email(parent_email, "Locker Application Successful",
                           f"Your application for {sel_student} has been successful. Locker {locker_number} assigned.")
            messagebox.showinfo("Success", f"Locker {locker_number} booked for student.")
            refresh_parent_students()
            refresh_lockers()
        else:
            # No lockers available: add to waiting list (booking with NULL locker_id)
            execute("INSERT INTO bookings (parent_id, student_id, locker_id, booking_date, payment_status) VALUES (%s,%s,%s,%s,%s)",
                    (parent_id, sid, None, date.today().isoformat(), "Unpaid"))
            simulate_email(parent_email, "Locker Application Waitlisted",
                           f"Your application for {sel_student} has been placed on the waiting list. We'll notify you if a locker becomes available.")
            messagebox.showinfo("Waitlisted", "No lockers available. Student added to waiting list.")
            refresh_parent_students()

    # Cancel application
    def cancel_application():
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Select", "Please select a student row to cancel application.")
            return
        item = tree.item(sel[0])['values']
        student_id = item[0]
        # find the current/latest booking for this student
        booking = fetchone("SELECT booking_id, locker_id FROM bookings WHERE student_id=%s ORDER BY booking_id DESC LIMIT 1", (student_id,))
        if not booking:
            messagebox.showinfo("No Application", "No booking/application found to cancel.")
            return
        booking_id, locker_id = booking
        # delete booking
        execute("DELETE FROM bookings WHERE booking_id=%s", (booking_id,))
        if locker_id is not None:
            # free the locker
            execute("UPDATE lockers SET status='Available' WHERE locker_id=%s", (locker_id,))
            # attempt to allocate freed locker to earliest waiting booking
            attempt_allocate_waitlist(locker_id)
        simulate_email(parent_email, "Locker Application Cancelled", f"Your application (Booking ID {booking_id}) has been cancelled.")
        messagebox.showinfo("Cancelled", "Application cancelled.")
        refresh_parent_students()
        refresh_lockers()

    # attach buttons
    btn_frame = tk.Frame(pwin)
    btn_frame.pack(pady=8, anchor="w", padx=10)

    tk.Button(btn_frame, text="Send Application", command=apply_for_locker).grid(row=0, column=0, padx=6)
    tk.Button(btn_frame, text="Check Application Outcome", command=check_application_outcome).grid(row=0, column=1, padx=6)
    tk.Button(btn_frame, text="Cancel Application", command=cancel_application).grid(row=0, column=2, padx=6)
    tk.Button(btn_frame, text="Refresh", command=lambda: (refresh_parent_students(), refresh_lockers(), refresh_student_combo())).grid(row=0, column=3, padx=6)

    # waiting list: admin may add or free lockers; we keep the parent side simple.

# -------------------------
# Waitlist management
# -------------------------
def attempt_allocate_waitlist(freed_locker_id=None):
    """
    If a locker becomes available (either freed_locker_id provided or any available),
    allocate it to the earliest booking with locker_id IS NULL (waiting list).
    """
    # If freed_locker_id is None, try to get any available locker
    if freed_locker_id:
        locker_row = fetchone("SELECT locker_id, locker_number FROM lockers WHERE locker_id=%s AND status='Available'", (freed_locker_id,))
        if not locker_row:
            return False
        locker_id, locker_number = locker_row
    else:
        av = fetchall("SELECT locker_id, locker_number FROM lockers WHERE status='Available' ORDER BY locker_number LIMIT 1")
        if not av:
            return False
        locker_id, locker_number = av[0]

    # find earliest waiting booking (first by booking_id) that has locker_id IS NULL
    waiting = fetchone("SELECT booking_id, parent_id, student_id FROM bookings WHERE locker_id IS NULL ORDER BY booking_id LIMIT 1")
    if not waiting:
        return False
    booking_id, parent_id, student_id = waiting
    # assign locker to booking
    execute("UPDATE bookings SET locker_id=%s, booking_date=%s WHERE booking_id=%s", (locker_id, date.today().isoformat(), booking_id))
    execute("UPDATE lockers SET status='Booked' WHERE locker_id=%s", (locker_id,))
    # notify parent of successful allocation
    parent_email_row = fetchone("SELECT email FROM parents WHERE parent_id=%s", (parent_id,))
    to_email = parent_email_row[0] if parent_email_row else "parent.test@amandla-school.org"
    simulate_email(to_email, "Locker Allocation Notice",
                   f"Good news — a locker ({locker_number}) became available and has been allocated to your student (Booking ID {booking_id}).")
    return True

# -------------------------
# Admin Dashboard
# -------------------------
def open_admin_dashboard():
    awin = tk.Toplevel(root)
    awin.title("Admin Dashboard - Locker Management & Payments")
    awin.geometry("980x560")

    tk.Label(awin, text="Administrator Dashboard", font=("Helvetica", 14, "bold")).pack(pady=8)

    # Table of all students and booking info
    cols = ("BookingID", "StudentID", "Student", "Grade", "Parent", "Locker", "AppStatus", "Payment")
    tree = ttk.Treeview(awin, columns=cols, show="headings", height=18)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120 if col != "Student" else 160)
    tree.pack(padx=10, pady=6)

    def refresh_admin_table():
        for i in tree.get_children():
            tree.delete(i)
        rows = fetchall('''
            SELECT b.booking_id,
                   s.student_id,
                   CONCAT(s.first_name, ' ', s.last_name),
                   s.grade,
                   CONCAT(p.first_name, ' ', p.last_name),
                   l.locker_number,
                   CASE WHEN b.locker_id IS NULL THEN 'Waitlisted' ELSE 'Booked' END,
                   COALESCE(b.payment_status, 'Unpaid')
            FROM bookings b
            JOIN students s ON b.student_id = s.student_id
            LEFT JOIN parents p ON b.parent_id = p.parent_id
            LEFT JOIN lockers l ON b.locker_id = l.locker_id
            ORDER BY b.booking_id
        ''')
        for r in rows:
            # r tuple may have fewer columns if CONCAT unsupported; ensure ordering
            booking_id = r[0]
            student_id = r[1]
            student_name = r[2]
            grade = r[3]
            parent_name = r[4]
            locker = r[5] if r[5] is not None else ""
            appstatus = r[6]
            payment = r[7]
            tree.insert("", "end", values=(booking_id, student_id, student_name, grade, parent_name, locker, appstatus, payment))

    refresh_admin_table()

    # Controls
    ctrl_frame = tk.Frame(awin)
    ctrl_frame.pack(pady=8)

    tk.Label(ctrl_frame, text="Payment Status:").grid(row=0, column=0, padx=6)
    status_var = tk.StringVar(value="Paid")
    status_combo = ttk.Combobox(ctrl_frame, textvariable=status_var, values=["Paid", "Unpaid"], state="readonly", width=12)
    status_combo.grid(row=0, column=1, padx=6)

    def update_payment_status():
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Select", "Please select a booking row to update.")
            return
        item = tree.item(sel[0])['values']
        booking_id = item[0]
        new_status = status_var.get()
        execute("UPDATE bookings SET payment_status=%s WHERE booking_id=%s", (new_status, booking_id))
        messagebox.showinfo("Updated", "Payment status updated.")
        refresh_admin_table()

    def approve_application():
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Select", "Please select a booking row to approve.")
            return
        item = tree.item(sel[0])['values']
        booking_id = item[0]
        appstatus = item[6]
        if appstatus != "Waitlisted":
            messagebox.showinfo("Info", "This booking is already allocated a locker.")
            return
        # find an available locker
        avail = fetchone("SELECT locker_id, locker_number FROM lockers WHERE status='Available' ORDER BY locker_number LIMIT 1")
        if not avail:
            messagebox.showwarning("No Lockers", "No available lockers to approve this application.")
            return
        locker_id, locker_number = avail
        # assign
        execute("UPDATE bookings SET locker_id=%s WHERE booking_id=%s", (locker_id, booking_id))
        execute("UPDATE lockers SET status='Booked' WHERE locker_id=%s", (locker_id,))
        # notify parent
        parent_email = fetchone('SELECT p.email FROM parents p JOIN bookings b ON p.parent_id = b.parent_id WHERE b.booking_id = %s', (booking_id,))
        to_email = parent_email[0] if parent_email else "parent.test@amandla-school.org"
        simulate_email(to_email, "Application Approved", f"Your student's locker application (Booking ID {booking_id}) has been approved. Assigned locker: {locker_number}.")
        messagebox.showinfo("Approved", f"Booking {booking_id} assigned locker {locker_number}.")
        refresh_admin_table()

    def reject_application():
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Select", "Please select a booking row to reject.")
            return
        item = tree.item(sel[0])['values']
        booking_id = item[0]
        # fetch parent email
        parent_email = fetchone('SELECT p.email FROM parents p JOIN bookings b ON p.parent_id = b.parent_id WHERE b.booking_id = %s', (booking_id,))
        to_email = parent_email[0] if parent_email else "parent.test@amandla-school.org"
        # delete booking
        execute("DELETE FROM bookings WHERE booking_id=%s", (booking_id,))
        simulate_email(to_email, "Application Rejected", f"Your student's locker application (Booking ID {booking_id}) has been rejected by administration.")
        messagebox.showinfo("Rejected", "Booking removed.")
        refresh_admin_table()

    def manual_allocate_waitlist():
        # attempt to allocate all available lockers to waiting list in FIFO order
        allocated = 0
        while True:
            av = fetchone("SELECT locker_id FROM lockers WHERE status='Available' ORDER BY locker_number LIMIT 1")
            if not av:
                break
            locker_id = av[0]
            ok = attempt_allocate_waitlist(locker_id)
            if not ok:
                break
            allocated += 1
        messagebox.showinfo("Allocation", f"Allocated {allocated} waiting application(s) where possible.")
        refresh_admin_table()

    tk.Button(ctrl_frame, text="Update Status", command=update_payment_status, bg="#1976D2", fg="white").grid(row=0, column=2, padx=6)
    tk.Button(ctrl_frame, text="Approve Application", command=approve_application).grid(row=0, column=3, padx=6)
    tk.Button(ctrl_frame, text="Reject Application", command=reject_application).grid(row=0, column=4, padx=6)
    tk.Button(ctrl_frame, text="Allocate Waitlist", command=manual_allocate_waitlist).grid(row=0, column=5, padx=6)
    tk.Button(ctrl_frame, text="Refresh", command=refresh_admin_table).grid(row=0, column=6, padx=6)

    # logout
    tk.Button(awin, text="Logout", command=awin.destroy, bg="#C62828", fg="white").pack(side="bottom", pady=8)

# -------------------------
# Login handling
# -------------------------
def login():
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    role = role_var.get()

    if role == "Administrator":
        # admin login uses admins table: match username or email to provided string and check password
        admin = fetchone("SELECT admin_id, username, password FROM admins WHERE (username=%s OR username=%s OR username=%s) LIMIT 1", (email, email, email))
        # NOTE: your admins table may not have email column. We check username only in this simple approach.
        # For safety, check explicit admin credentials:
        if email == "admin@amandla.local" and password == "admin123":
            messagebox.showinfo("Login Success", "Welcome Administrator!")
            open_admin_dashboard()
            return
        # fallback: check admins table username + password
        admin_row = fetchone("SELECT admin_id FROM admins WHERE (username=%s OR username=%s) AND password=%s LIMIT 1", (email, email, password))
        if admin_row:
            messagebox.showinfo("Login Success", "Welcome Administrator!")
            open_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid administrator credentials.")
    else:
        # Parent login: email must exist in parents table; password check is simulated: default password is 'parentpass'
        p = fetchone("SELECT parent_id, email FROM parents WHERE email=%s", (email,))
        if p is None:
            messagebox.showerror("Login Failed", "No parent account found with that email.")
            return
        # check simulated password
        if password != "parentpass":
            messagebox.showerror("Login Failed", "Invalid password for parent accounts. Default password = parentpass")
            return
        messagebox.showinfo("Login Success", f"Welcome Parent ({email})!")
        open_parent_dashboard(email)

login_btn = tk.Button(frame, text="Login", command=login)
login_btn.pack(pady=10)

# Start mainloop
root.mainloop()
