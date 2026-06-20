
import tkinter as tk
from tkinter import ttk, messagebox



patients = []
doctors = []
appointments = []



def make_treeview(parent, columns):
    tree = ttk.Treeview(parent, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=150, anchor="center")
    return tree



class LoginWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Login - Hospital Management System")
        self.geometry("500x350")
        self.resizable(False, False)
        self.configure(bg="#d9e4f5")

        self.create_login_ui()

    
    def create_login_ui(self):
        tk.Label(self, text="LOGIN", font=("Arial", 26, "bold"), bg="#d9e4f5").pack(pady=20)

        main_frame = tk.Frame(self, bg="#d9e4f5")
        main_frame.pack()

        tk.Label(main_frame, text="Username:", font=("Arial", 14), bg="#d9e4f5").grid(row=0, column=0, pady=10)
        tk.Label(main_frame, text="Password:", font=("Arial", 14), bg="#d9e4f5").grid(row=1, column=0, pady=10)

        self.username_entry = tk.Entry(main_frame, font=("Arial", 14))
        self.password_entry = tk.Entry(main_frame, font=("Arial", 14), show="*")

        self.username_entry.grid(row=0, column=1, padx=10)
        self.password_entry.grid(row=1, column=1, padx=10)

        login_btn = tk.Button(self, text="LOGIN", font=("Arial", 16),
                              command=self.check_login, bg="#4a90e2", fg="white", width=15)
        login_btn.pack(pady=20)

  
    def check_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()

        if user == "PRAJITH" and pwd == "12345":
            messagebox.showinfo("Success", "Login Successful!")
            self.destroy()
            HospitalSystem()   # open second page
        else:
            messagebox.showerror("Error", "Invalid Username or Password")



class HospitalSystem:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hospital Management System")
        self.root.geometry("1300x750")
        self.root.configure(bg="#eef2f3")
        self.root.resizable(False, False)

        self.create_layout()

        self.root.mainloop()

   
    def create_layout(self):
        title = tk.Label(self.root, text="🏥 Hospital Management System",
                         font=("Arial", 26, "bold"), bg="#eef2f3")
        title.pack(pady=20)

        tabs = ttk.Notebook(self.root)
        tabs.pack(expand=True, fill="both")

        self.patient_tab = tk.Frame(tabs, bg="white")
        self.doctor_tab = tk.Frame(tabs, bg="white")
        self.appointment_tab = tk.Frame(tabs, bg="white")

        tabs.add(self.patient_tab, text="Patients")
        tabs.add(self.doctor_tab, text="Doctors")
        tabs.add(self.appointment_tab, text="Appointments")

        self.create_patient_tab()
        self.create_doctor_tab()
        self.create_appointment_tab()

   
    def create_patient_tab(self):

        tk.Label(self.patient_tab, text="Patient Details",
                 font=("Arial", 22, "bold"), bg="white").pack(pady=20)

        form = tk.Frame(self.patient_tab, bg="white")
        form.pack()

        # Form Labels & Entry fields
        labels = ["Name", "Age", "Gender", "Contact", "Email", "Address", "Disease"]
        self.p_entries = {}

        for i, text in enumerate(labels):
            tk.Label(form, text=text, font=("Arial", 14), bg="white").grid(row=i, column=0, pady=8, sticky="w")
            entry = tk.Entry(form, font=("Arial", 14), width=27)
            entry.grid(row=i, column=1, padx=20)
            self.p_entries[text.lower()] = entry

        self.patient_buttons(form)
        self.patient_table()

   
    def patient_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="white")
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Add", width=12, font=("Arial", 12),
                  command=self.add_patient).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="View", width=12, font=("Arial", 12),
                  command=self.view_patients).grid(row=0, column=1, padx=10)

        tk.Button(button_frame, text="Search", width=12, font=("Arial", 12),
                  command=self.search_patient).grid(row=0, column=2, padx=10)

        tk.Button(button_frame, text="Delete", width=12, font=("Arial", 12),
                  command=self.delete_patient).grid(row=0, column=3, padx=10)

        tk.Button(button_frame, text="Clear", width=12, font=("Arial", 12),
                  command=self.clear_patient).grid(row=0, column=4, padx=10)

   
    def patient_table(self):
        columns = ["Name", "Age", "Gender", "Contact", "Email", "Address", "Disease"]

        self.patient_tree = make_treeview(self.patient_tab, columns)
        self.patient_tree.pack(pady=20)

    
    def add_patient(self):
        data = {k: v.get() for k, v in self.p_entries.items()}
        patients.append(data)
        messagebox.showinfo("Success", "Patient Added!")

    def view_patients(self):
        for row in self.patient_tree.get_children():
            self.patient_tree.delete(row)

        for p in patients:
            self.patient_tree.insert("", "end", values=list(p.values()))

    def search_patient(self):
        name = self.p_entries["name"].get().lower()

        for row in self.patient_tree.get_children():
            self.patient_tree.delete(row)

        for p in patients:
            if name in p["name"].lower():
                self.patient_tree.insert("", "end", values=list(p.values()))

    def delete_patient(self):
        sel = self.patient_tree.focus()
        if not sel:
            return

        name = self.patient_tree.item(sel)["values"][0]
        global patients
        patients = [p for p in patients if p["name"] != name]

        self.view_patients()
        messagebox.showinfo("Info", "Patient Deleted!")

    def clear_patient(self):
        for entry in self.p_entries.values():
            entry.delete(0, tk.END)

   
    def create_doctor_tab(self):

        tk.Label(self.doctor_tab, text="Doctor Details",
                 font=("Arial", 22, "bold"), bg="white").pack(pady=20)

        form = tk.Frame(self.doctor_tab, bg="white")
        form.pack()

        labels = ["Name", "Department", "Contact"]
        self.d_entries = {}

        for i, text in enumerate(labels):
            tk.Label(form, text=text, font=("Arial", 14), bg="white").grid(row=i, column=0, pady=8, sticky="w")
            entry = tk.Entry(form, font=("Arial", 14), width=27)
            entry.grid(row=i, column=1, padx=20)
            self.d_entries[text.lower()] = entry

        self.doctor_buttons(form)
        self.doctor_table()


    def doctor_buttons(self, parent):
        frame = tk.Frame(parent, bg="white")
        frame.grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(frame, text="Add", width=12, font=("Arial", 12),
                  command=self.add_doctor).grid(row=0, column=0, padx=10)

        tk.Button(frame, text="View", width=12, font=("Arial", 12),
                  command=self.view_doctors).grid(row=0, column=1, padx=10)

        tk.Button(frame, text="Search", width=12, font=("Arial", 12),
                  command=self.search_doctor).grid(row=0, column=2, padx=10)

        tk.Button(frame, text="Delete", width=12, font=("Arial", 12),
                  command=self.delete_doctor).grid(row=0, column=3, padx=10)

   
    def doctor_table(self):
        columns = ["Name", "Department", "Contact"]

        self.doctor_tree = make_treeview(self.doctor_tab, columns)
        self.doctor_tree.pack(pady=20)

   
    def add_doctor(self):
        data = {k: v.get() for k, v in self.d_entries.items()}
        doctors.append(data)
        messagebox.showinfo("Success", "Doctor Added!")

    def view_doctors(self):
        for row in self.doctor_tree.get_children():
            self.doctor_tree.delete(row)

        for d in doctors:
            self.doctor_tree.insert("", "end", values=list(d.values()))

    def search_doctor(self):
        name = self.d_entries["name"].get().lower()

        for row in self.doctor_tree.get_children():
            self.doctor_tree.delete(row)

        for d in doctors:
            if name in d["name"].lower():
                self.doctor_tree.insert("", "end", values=list(d.values()))

    def delete_doctor(self):
        sel = self.doctor_tree.focus()
        if not sel:
            return

        name = self.doctor_tree.item(sel)["values"][0]
        global doctors
        doctors = [d for d in doctors if d["name"] != name]

        self.view_doctors()
        messagebox.showinfo("Info", "Doctor Deleted!")

   
    def create_appointment_tab(self):

        tk.Label(self.appointment_tab, text="Appointment Details",
                 font=("Arial", 22, "bold"), bg="white").pack(pady=20)

        form = tk.Frame(self.appointment_tab, bg="white")
        form.pack()

        labels = ["Patient", "Doctor", "Date", "Time", "Status", "Notes"]
        self.a_entries = {}

        for i, text in enumerate(labels):
            tk.Label(form, text=text, font=("Arial", 14), bg="white").grid(row=i, column=0, pady=8, sticky="w")
            entry = tk.Entry(form, font=("Arial", 14), width=27)
            entry.grid(row=i, column=1, padx=20)
            self.a_entries[text.lower()] = entry

        self.appointment_buttons(form)
        self.appointment_table()

    
    def appointment_buttons(self, parent):
        frame = tk.Frame(parent, bg="white")
        frame.grid(row=6, column=0, columnspan=2, pady=20)

        tk.Button(frame, text="Add", width=12, font=("Arial", 12),
                  command=self.add_appointment).grid(row=0, column=0, padx=10)

        tk.Button(frame, text="View", width=12, font=("Arial", 12),
                  command=self.view_appointments).grid(row=0, column=1, padx=10)

        tk.Button(frame, text="Search", width=12, font=("Arial", 12),
                  command=self.search_appointment).grid(row=0, column=2, padx=10)

        tk.Button(frame, text="Delete", width=12, font=("Arial", 12),
                  command=self.delete_appointment).grid(row=0, column=3, padx=10)

    
    def appointment_table(self):
        columns = ["Patient", "Doctor", "Date", "Time", "Status", "Notes"]

        self.appt_tree = make_treeview(self.appointment_tab, columns)
        self.appt_tree.pack(pady=20)

   
    def add_appointment(self):
        data = {k: v.get() for k, v in self.a_entries.items()}
        appointments.append(data)
        messagebox.showinfo("Success", "Appointment Added!")

    def view_appointments(self):
        for row in self.appt_tree.get_children():
            self.appt_tree.delete(row)

        for a in appointments:
            self.appt_tree.insert("", "end", values=list(a.values()))

    def search_appointment(self):
        name = self.a_entries["patient"].get().lower()

        for row in self.appt_tree.get_children():
            self.appt_tree.delete(row)

        for a in appointments:
            if name in a["patient"].lower():
                self.appt_tree.insert("", "end", values=list(a.values()))

    def delete_appointment(self):
        sel = self.appt_tree.focus()
        if not sel:
            return

        name = self.appt_tree.item(sel)["values"][0]
        global appointments
        appointments = [a for a in appointments if a["patient"] != name]

        self.view_appointments()
        messagebox.showinfo("Info", "Appointment Deleted!")



if __name__ == "__main__":
    LoginWindow()
