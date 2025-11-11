from datetime import date
import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk

# Create new SQLite database
conn = sqlite3.connect('system.db')
cursor = conn.cursor()

# Read SQL file
with open(r"C:\Users\nisha\Desktop\ICT3715 Database and Code\Database\amandla_locker_system.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Execute all SQL commands
cursor.executescript(sql_script)
conn.commit()
conn.close()

def connect_db():
    return sqlite3.connector.connect(
        host="localhost",
        user="root",       # change if you use another MySQL username
        password="Bat2-3man",        # add your MySQL password if set
        database="amandla_locker_system"
    )

def login():
    user = email_entry.get()
    pwd = password_entry.get()

    conn = connect_db()
    cursor = conn.cursor()

    # Update this query if your table or column names differ
    cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (user, pwd))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Success", f"Welcome {user}!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

    conn.close()

print("Database imported successfully!")


# --- Login Function ---
def login():
    email = email_entry.get()
    password = password_entry.get()  # optional, if you add password column
    role = role_var.get()

    conn = sqlite3.connect('system.db')
    if conn:
        cursor = conn.cursor()
        # Check in database if user exists (adjust table/columns if needed)
        if role == "Parent":
            query = "SELECT * FROM parents WHERE email=?"
        else:
            query = "SELECT * FROM admins WHERE email=?"

        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Login Success", f"Welcome {role}!")
            root.destroy()  # Close login window
            # Here you can open the Parent or Admin Dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
        conn.close()


# --- GUI ---
root = tk.Tk()
root.title("Amandla High School - Locker Booking (Login)")
root.geometry("420x360")
root.resizable(False, False)

# Frame layout
frame = tk.Frame(root, padx=15, pady=15)
frame.pack(expand=True, fill="both")

title = tk.Label(frame, text="Locker Booking System - Login", font=("Helvetica", 14, "bold"))
title.pack(pady=(0,10))

# Email
tk.Label(frame, text="Email:").pack(anchor="w")
email_entry = tk.Entry(frame, width=40)
email_entry.pack(pady=3)

# Password
tk.Label(frame, text="Password:").pack(anchor="w")
password_entry = tk.Entry(frame, width=40, show="*")
password_entry.pack(pady=3)

# Role
tk.Label(frame, text="Login as:").pack(anchor="w")
role_var = tk.StringVar(value="Parent")
role_combo = ttk.Combobox(frame, textvariable=role_var, values=["Parent", "Administrator"], state="readonly", width=37)
role_combo.pack(pady=5)

info_label = tk.Label(frame, text="Admin: admin@amandla.local / admin123\nParent accounts use parent email; default password = parentpass", font=("Helvetica", 8), fg="gray")
info_label.pack(pady=(6,8))

# Login function
root = tk.Tk()
root.title("Amandla High School Locker System Login")
root.geometry("400x300")

tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.pack()

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack()

tk.Label(root, text="Role:").pack(pady=5)
role_var = tk.StringVar(value="Parent")
tk.Radiobutton(root, text="Parent", variable=role_var, value="Parent").pack()
tk.Radiobutton(root, text="Administrator", variable=role_var, value="Administrator").pack()

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()

# ---------------- Parent Dashboard ----------------
def open_parent_dashboard(parent_email):
    conn = sqlite3.connect('system.db')
    c = conn.cursor()
    c.execute("SELECT parent_id, first_name, last_name FROM parents WHERE email = ?", (parent_email,))
    parent = c.fetchone()
    if not parent:
        messagebox.showerror("Error", "Parent record not found")
        conn.close()
        return
    parent_id = parent[0]
    parent_name = f"{parent[1]} {parent[2]}"

    pwin = tk.Toplevel(root)
    pwin.title("Parent Dashboard - Locker Booking")
    pwin.geometry("640x420")

    tk.Label(pwin, text=f"Parent Dashboard — {parent_name}", font=("Helvetica", 13, "bold")).pack(pady=8)
    tk.Label(pwin, text="Your Students:", font=("Helvetica", 11, "underline")).pack(anchor="w", padx=10)

    # Student list
    cols = ("StudentID", "SchoolNo", "Name", "Surname", "Grade", "Locker")
    tree = ttk.Treeview(pwin, columns=cols, show="headings", height=8)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(padx=10, pady=(4,8))

    c.execute("SELECT s.student_id, s.school_number, s.first_name, s.last_name, s.grade, l.locker_number FROM students s LEFT JOIN bookings b ON s.student_id=b.student_id LEFT JOIN lockers l ON b.locker_id=l.locker_id WHERE s.parent_id = ?", (parent_id,))
    rows = c.fetchall()
    for r in rows:
        tree.insert("", "end", values=r)

    # Locker selection
    tk.Label(pwin, text="Available Lockers:").pack(anchor="w", padx=10)
    c.execute("SELECT locker_id, locker_number FROM lockers WHERE status='Available' LIMIT 50")
    lockers = c.fetchall()
    locker_map = {f"{ln}": lid for lid, ln in lockers}
    locker_vals = list(locker_map.keys())

    locker_var = tk.StringVar()
    locker_combo = ttk.Combobox(pwin, textvariable=locker_var, values=locker_vals, width=20)
    locker_combo.pack(padx=10, pady=6, anchor="w")

    # Student select
    tk.Label(pwin, text="Select Student to assign locker:").pack(anchor="w", padx=10)
    student_var = tk.StringVar()
    student_combo = ttk.Combobox(pwin, textvariable=student_var, values=[f"{r[2]} {r[3]} (ID {r[0]})" for r in rows], width=28)
    student_combo.pack(padx=10, pady=6, anchor="w")

    def confirm_booking():
        sel_locker = locker_var.get()
        sel_student = student_var.get()
        if not sel_locker or not sel_student:
            messagebox.showerror("Missing", "Select a locker and a student")
            return
        # parse student id
        sid = int(sel_student.split("ID")[-1].strip(" )"))
        lid = locker_map.get(sel_locker)
        if not lid:
            messagebox.showerror("Error", "Locker selection invalid or taken. Refresh and try again.")
            return
        conn2 = sqlite3.connect('system.db')
        c2 = conn2.cursor()
        # create booking
        c2.execute("INSERT INTO bookings (parent_id, student_id, locker_id, booking_date, payment_status) VALUES (?,?,?,?,?)",
                   (parent_id, sid, lid, date.today().isoformat(), "Unpaid"))
        # mark locker
        c2.execute("UPDATE lockers SET status=?, assigned_student_id=? WHERE locker_id=?", ("Booked", sid, lid))
        conn2.commit()
        conn2.close()
        messagebox.showinfo("Booked", f"{sel_locker} booked for student.")
        pwin.destroy()

    tk.Button(pwin, text="Confirm Booking", command=confirm_booking, bg="#2E7D2", fg="white").pack(pady=10, anchor="w", padx=10)

    tk.Button(pwin, text="Logout", command=pwin.destroy, bg="#C62828", fg="white").pack(side="bottom", pady=10)

    conn.close()

# ---------------- Admin Dashboard ----------------
def open_admin_dashboard():
    awin = tk.Toplevel(root)
    awin.title("Admin Dashboard - Locker Management & Payments")
    awin.geometry("900x520")

    tk.Label(awin, text="Administrator Dashboard", font=("Helvetica", 14, "bold")).pack(pady=8)

    # Table of all students and payment status
    cols = ("StudentID", "Student", "Grade", "Parent", "Locker", "Payment")
    tree = ttk.Treeview(awin, columns=cols, show="headings", height=18)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=140 if col!="StudentID" else 80)
    tree.pack(padx=10, pady=6)

    conn = sqlite3.connect('system.db')
    c = conn.cursor()
    c.execute('''
        SELECT s.student_id, s.first_name || ' ' || s.last_name, s.grade,
               p.first_name || ' ' || p.last_name, l.locker_number,
               COALESCE(b.payment_status, 'Unpaid')
        FROM students s
        LEFT JOIN parents p ON s.parent_id = p.parent_id
        LEFT JOIN bookings b ON s.student_id = b.student_id
        LEFT JOIN lockers l ON b.locker_id = l.locker_id
        ORDER BY s.student_id
    ''')
    for row in c.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

    # payment update controls
    ctrl_frame = tk.Frame(awin)
    ctrl_frame.pack(pady=8)

    tk.Label(ctrl_frame, text="New Payment Status:").grid(row=0, column=0, padx=6)
    status_var = tk.StringVar(value="Paid")
    status_combo = ttk.Combobox(ctrl_frame, textvariable=status_var, values=["Paid", "Unpaid"], state="readonly", width=12)
    status_combo.grid(row=0, column=1, padx=6)

    def update_payment_status():
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Select", "Please select a student row to update")
            return
        new_status = status_var.get()
        item = tree.item(sel[0])['values']
        student_id = item[0]
        # find booking for that student
        conn2 = sqlite3.connect('system.db')
        c2 = conn2.cursor()
        c2.execute("SELECT booking_id FROM bookings WHERE student_id = ?", (student_id,))
        r = c2.fetchone()
        if r:
            booking_id = r[0]
            c2.execute("UPDATE bookings SET payment_status=? WHERE booking_id=?", (new_status, booking_id))
            conn2.commit()
            messagebox.showinfo("Updated", "Payment status updated")
        else:
            messagebox.showwarning("No booking", "No booking record for this student. Create a booking first if appropriate.")
        conn2.close()
        # refresh table
        awin.destroy()
        open_admin_dashboard()

    tk.Button(ctrl_frame, text="Update Status", command=update_payment_status, bg="#1976D2", fg="white").grid(row=0, column=2, padx=6)
    tk.Button(awin, text="Logout", command=awin.destroy, bg="#C62828", fg="white").pack(side="bottom", pady=8)

# Start mainloop
root.mainloop()