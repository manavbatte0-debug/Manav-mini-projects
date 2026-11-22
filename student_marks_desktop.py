import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# ============================================================
# STUDENT MARKS MANAGEMENT SYSTEM - DARK DESKTOP EDITION
# Uses only Python standard-library modules (Tkinter + JSON).
# ============================================================

SUBJECTS = ("English", "Mathematics", "Science", "Computer")
BASE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "StudentMarks")
FILE_NAME = os.path.join(BASE_DIR, "student_records.json")

students = []

# Dark theme palette
BG = "#0b1120"
SIDEBAR = "#101a2d"
PANEL = "#141f33"
PANEL_ALT = "#19263d"
BORDER = "#263650"
TEXT = "#e8eef8"
MUTED = "#91a0b8"
ACCENT = "#6c8cff"
ACCENT_HOVER = "#5578ee"
GREEN = "#35c98a"
RED = "#ff6b78"
YELLOW = "#f4c66a"


def load_records():
    """Load existing JSON records. Existing data format is preserved."""
    global students
    if not os.path.exists(FILE_NAME):
        students = []
        return
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list):
            # Keep only well-formed records and ensure all subjects exist.
            students = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                marks = item.get("marks", {})
                if not isinstance(marks, dict):
                    marks = {}
                normalized = {
                    "roll_no": str(item.get("roll_no", "")),
                    "name": str(item.get("name", "")),
                    "marks": {subject: float(marks.get(subject, 0)) for subject in SUBJECTS}
                }
                students.append(normalized)
        else:
            students = []
            messagebox.showwarning("Records", "The records file has an invalid format. Starting with an empty list.")
    except (json.JSONDecodeError, OSError, TypeError, ValueError) as error:
        students = []
        messagebox.showerror("Could not load records", str(error))


def save_records():
    """Save records to the same JSON location used by the original project."""
    try:
        os.makedirs(BASE_DIR, exist_ok=True)
        temp_file = FILE_NAME + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
        os.replace(temp_file, FILE_NAME)
        return True
    except (OSError, TypeError) as error:
        messagebox.showerror(
            "Could not save records",
            f"{error}\n\nSave location:\n{FILE_NAME}"
        )
        return False


def calculate_result(marks):
    total = sum(float(marks.get(subject, 0)) for subject in SUBJECTS)
    percentage = total / len(SUBJECTS)
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"
    return total, percentage, grade


class StudentMarksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Marks Management System")
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)
        self.root.configure(bg=BG)

        self.current_page = "Dashboard"
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self._configure_styles()
        self._build_shell()
        self.show_page("Dashboard")

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=PANEL,
            foreground=TEXT,
            fieldbackground=PANEL,
            rowheight=38,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=PANEL_ALT,
            foreground=MUTED,
            relief="flat",
            borderwidth=0,
            font=("Segoe UI Semibold", 9)
        )
        style.map(
            "Treeview",
            background=[("selected", "#294477")],
            foreground=[("selected", "#ffffff")]
        )
        style.map("Treeview.Heading", background=[("active", PANEL_ALT)])
        style.configure(
            "Vertical.TScrollbar",
            background=PANEL_ALT,
            troughcolor=PANEL,
            bordercolor=PANEL,
            arrowcolor=MUTED
        )

    def _build_shell(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(27, 34))
        tk.Label(brand, text="✦  STUDENT", bg=SIDEBAR, fg=TEXT,
                 font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(brand, text="MARKS MANAGEMENT", bg=SIDEBAR, fg=ACCENT,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=(27, 0), pady=(2, 0))

        tk.Label(self.sidebar, text="WORKSPACE", bg=SIDEBAR, fg="#63738d",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22, pady=(0, 10))

        self.nav_buttons = {}
        for label, symbol in [
            ("Dashboard", "▦"),
            ("Students", "♙"),
            ("Add Student", "+"),
            ("Topper", "★"),
        ]:
            btn = tk.Button(
                self.sidebar, text=f"   {symbol}    {label}",
                command=lambda page=label: self.show_page(page),
                anchor="w", relief="flat", bd=0, cursor="hand2",
                bg=SIDEBAR, fg=MUTED, activebackground=PANEL_ALT,
                activeforeground=TEXT, font=("Segoe UI", 10),
                padx=12, pady=12
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[label] = btn

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(24, 16))
        tk.Label(self.sidebar, text="DATA STORAGE", bg=SIDEBAR, fg="#63738d",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22)
        tk.Label(self.sidebar, text="●  JSON file connected", bg=SIDEBAR, fg=GREEN,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=22, pady=(12, 4))
        tk.Label(self.sidebar, text="Documents / StudentMarks", bg=SIDEBAR,
                 fg=MUTED, font=("Segoe UI", 8), wraplength=180,
                 justify="left").pack(anchor="w", padx=22)
        tk.Label(self.sidebar, text="Student Marks v1.0", bg=SIDEBAR, fg="#63738d",
                 font=("Segoe UI", 8)).pack(side="bottom", anchor="w", padx=22, pady=20)

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        header = tk.Frame(self.main, bg=BG)
        header.pack(fill="x", padx=32, pady=(25, 18))
        self.page_title = tk.Label(header, text="Dashboard", bg=BG, fg=TEXT,
                                   font=("Segoe UI", 22, "bold"))
        self.page_title.pack(side="left")
        tk.Label(header, text="ACADEMIC OVERVIEW", bg=BG, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(side="right", pady=10)

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=32, pady=(0, 10))

        footer = tk.Frame(self.main, bg=BG)
        footer.pack(fill="x", padx=32, pady=(0, 14))
        tk.Label(footer, textvariable=self.status_var, bg=BG, fg=MUTED,
                 font=("Segoe UI", 8)).pack(side="left")
        tk.Label(footer, text="Local desktop application  •  Offline data storage",
                 bg=BG, fg="#63738d", font=("Segoe UI", 8)).pack(side="right")

    def _clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _card(self, parent, title, value, subtitle, accent=ACCENT):
        card = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        tk.Frame(card, bg=accent, height=3).pack(fill="x")
        inner = tk.Frame(card, bg=PANEL)
        inner.pack(fill="both", expand=True, padx=18, pady=15)
        tk.Label(inner, text=title.upper(), bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(inner, text=value, bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 23, "bold")).pack(anchor="w", pady=(8, 2))
        tk.Label(inner, text=subtitle, bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8)).pack(anchor="w")
        return card

    def _section_title(self, parent, title, description=None):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(0, 12))
        tk.Label(row, text=title, bg=BG, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        if description:
            tk.Label(row, text=description, bg=BG, fg=MUTED,
                     font=("Segoe UI", 8)).pack(side="right")
        return row

    def _button(self, parent, text, command, primary=True, width=None):
        return tk.Button(
            parent, text=text, command=command, cursor="hand2",
            relief="flat", bd=0, padx=16, pady=9, width=width,
            bg=ACCENT if primary else PANEL_ALT,
            fg="#ffffff" if primary else TEXT,
            activebackground=ACCENT_HOVER if primary else BORDER,
            activeforeground="#ffffff", font=("Segoe UI", 9, "bold")
        )

    def _make_table(self, parent, compact=False):
        columns = ("roll", "name", "total", "percentage", "grade")
        table_wrap = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        table_wrap.pack(fill="both", expand=True)
        table = ttk.Treeview(table_wrap, columns=columns, show="headings", selectmode="browse")
        headings = {
            "roll": ("ROLL NO.", 110),
            "name": ("STUDENT NAME", 230),
            "total": ("TOTAL", 100),
            "percentage": ("PERCENTAGE", 120),
            "grade": ("GRADE", 90),
        }
        for col, (heading, width) in headings.items():
            table.heading(col, text=heading)
            table.column(col, width=width, anchor="w" if col == "name" else "center")
        scrollbar = ttk.Scrollbar(table_wrap, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        table.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=8)
        table.tag_configure("odd", background=PANEL)
        table.tag_configure("even", background=PANEL_ALT)
        return table

    def _fill_table(self, table, records=None):
        for item in table.get_children():
            table.delete(item)
        records = students if records is None else records
        for index, student in enumerate(records):
            total, percentage, grade = calculate_result(student["marks"])
            table.insert(
                "", "end",
                values=(
                    student["roll_no"], student["name"],
                    f"{total:.0f} / 400", f"{percentage:.2f}%",
                    grade
                ),
                tags=("even" if index % 2 else "odd",)
            )

    def show_page(self, page):
        self.current_page = page
        self.page_title.config(text=page)
        for name, button in self.nav_buttons.items():
            button.config(bg=PANEL_ALT if name == page else SIDEBAR,
                          fg=TEXT if name == page else MUTED)
        self._clear_content()

        if page == "Dashboard":
            self._dashboard()
        elif page == "Students":
            self._students_page()
        elif page == "Add Student":
            self.open_student_form()
        elif page == "Topper":
            self._topper_page()

    def _dashboard(self):
        count = len(students)
        average = sum(calculate_result(s["marks"])[1] for s in students) / count if count else 0
        passed = sum(1 for s in students if calculate_result(s["marks"])[1] >= 40)
        topper = max(students, key=lambda s: calculate_result(s["marks"])[1]) if students else None
        topper_text = topper["name"] if topper else "—"

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=(0, 24))
        for i in range(4):
            cards.grid_columnconfigure(i, weight=1, uniform="cards")
        data = [
            ("Total Students", str(count), "Registered student records", ACCENT),
            ("Class Average", f"{average:.1f}%", "Average percentage", GREEN),
            ("Passed Students", str(passed), "Percentage 40% or above", YELLOW),
            ("Class Topper", topper_text, "Highest percentage", "#b18cff"),
        ]
        for i, item in enumerate(data):
            card = self._card(cards, *item)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 10, 0))

        action_row = tk.Frame(self.content, bg=BG)
        action_row.pack(fill="x", pady=(0, 22))
        tk.Label(action_row, text="Recent student records", bg=BG, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        self._button(action_row, "+ Add Student", lambda: self.show_page("Add Student")).pack(side="right")

        table = self._make_table(self.content)
        recent = sorted(students, key=lambda s: s["name"].lower())[:8]
        self._fill_table(table, recent)
        if not students:
            tk.Label(self.content, text="No student records yet. Select “Add Student” to create your first record.",
                     bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(pady=14)

    def _students_page(self):
        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0, 14))
        tk.Label(top, text="Manage student records and academic results.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(side="left")
        self._button(top, "+ Add Student", lambda: self.open_student_form()).pack(side="right")

        search_row = tk.Frame(self.content, bg=BG)
        search_row.pack(fill="x", pady=(0, 12))
        search_entry = tk.Entry(search_row, textvariable=self.search_var,
                                bg=PANEL, fg=TEXT, insertbackground=TEXT,
                                relief="flat", font=("Segoe UI", 10))
        search_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        search_entry.insert(0, "")
        self._button(search_row, "Search", self._search_table, primary=False).pack(side="left")
        self._button(search_row, "Clear", self._clear_search, primary=False).pack(side="left", padx=(7, 0))

        self.student_table = self._make_table(self.content)
        self._fill_table(self.student_table)

        actions = tk.Frame(self.content, bg=BG)
        actions.pack(fill="x", pady=14)
        self._button(actions, "View Details", self.view_selected, primary=False).pack(side="left")
        self._button(actions, "Edit Marks", self.edit_selected).pack(side="left", padx=8)
        self._button(actions, "Delete Student", self.delete_selected, primary=False).pack(side="left")

    def _search_table(self):
        query = self.search_var.get().strip().lower()
        matches = [
            s for s in students
            if query in s["roll_no"].lower() or query in s["name"].lower()
        ]
        self._fill_table(self.student_table, matches)
        self.status_var.set(f"{len(matches)} matching record(s)")

    def _clear_search(self):
        self.search_var.set("")
        self._fill_table(self.student_table)
        self.status_var.set("Showing all student records")

    def _selected_student(self):
        if not hasattr(self, "student_table"):
            return None
        selection = self.student_table.selection()
        if not selection:
            messagebox.showinfo("Select student", "Please select a student from the table.")
            return None
        roll = self.student_table.item(selection[0], "values")[0]
        return next((s for s in students if s["roll_no"] == str(roll)), None)

    def view_selected(self):
        student = self._selected_student()
        if student:
            total, percentage, grade = calculate_result(student["marks"])
            details = (
                f"Name: {student['name']}\n"
                f"Roll number: {student['roll_no']}\n\n"
                + "\n".join(f"{subject}: {student['marks'].get(subject, 0):g}" for subject in SUBJECTS)
                + f"\n\nTotal: {total:g} / 400\nPercentage: {percentage:.2f}%\nGrade: {grade}"
            )
            messagebox.showinfo("Student details", details)

    def edit_selected(self):
        student = self._selected_student()
        if student:
            self.open_student_form(student)

    def delete_selected(self):
        student = self._selected_student()
        if not student:
            return
        if not messagebox.askyesno("Confirm deletion", f"Delete {student['name']} ({student['roll_no']})?"):
            return
        index = students.index(student)
        removed = students.pop(index)
        if save_records():
            self.status_var.set(f"Deleted {removed['name']}")
            self.show_page("Students")
        else:
            students.insert(index, removed)

    def open_student_form(self, existing=None):
        editing = existing is not None
        title = "Edit student marks" if editing else "Add a new student"
        win = tk.Toplevel(self.root)
        win.title(title)
        win.configure(bg=BG)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        body = tk.Frame(win, bg=PANEL, padx=26, pady=24)
        body.pack(fill="both", expand=True, padx=16, pady=16)
        tk.Label(body, text=title, bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(body, text="Enter student information and marks out of 100.",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 18))

        form = tk.Frame(body, bg=PANEL)
        form.pack(fill="x")
        roll_var = tk.StringVar(value=existing["roll_no"] if editing else "")
        name_var = tk.StringVar(value=existing["name"] if editing else "")

        self._form_field(form, "Roll Number", roll_var, 0, disabled=editing)
        self._form_field(form, "Student Name", name_var, 1)

        mark_vars = {}
        initial_marks = existing["marks"] if editing else {}
        for index, subject in enumerate(SUBJECTS, start=2):
            var = tk.StringVar(value=str(initial_marks.get(subject, "")))
            mark_vars[subject] = var
            self._form_field(form, f"{subject} Marks (0–100)", var, index)

        def submit():
            roll = roll_var.get().strip()
            name = name_var.get().strip()
            if not roll or not name:
                messagebox.showwarning("Missing information", "Enter both roll number and student name.", parent=win)
                return
            if not editing and any(s["roll_no"] == roll for s in students):
                messagebox.showwarning("Duplicate roll number", "This roll number already exists.", parent=win)
                return
            marks = {}
            try:
                for subject, var in mark_vars.items():
                    value = float(var.get())
                    if not 0 <= value <= 100:
                        raise ValueError
                    marks[subject] = value
            except ValueError:
                messagebox.showwarning("Invalid marks", "Enter a number from 0 to 100 for every subject.", parent=win)
                return

            if editing:
                old = existing["marks"].copy()
                existing["marks"] = marks
                if not save_records():
                    existing["marks"] = old
                    return
                self.status_var.set(f"Updated marks for {name}")
            else:
                record = {"roll_no": roll, "name": name, "marks": marks}
                students.append(record)
                if not save_records():
                    students.pop()
                    return
                self.status_var.set(f"Added student {name}")

            win.destroy()
            self.show_page("Students")

        buttons = tk.Frame(body, bg=PANEL)
        buttons.pack(fill="x", pady=(20, 0))
        self._button(buttons, "Save Student" if not editing else "Save Changes", submit).pack(side="left")
        self._button(buttons, "Cancel", win.destroy, primary=False).pack(side="left", padx=8)

        win.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - win.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{max(0, x)}+{max(0, y)}")

    def _form_field(self, parent, label, variable, row, disabled=False):
        tk.Label(parent, text=label, bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=6)
        entry = tk.Entry(parent, textvariable=variable, width=34,
                         bg=PANEL_ALT, fg=TEXT, insertbackground=TEXT,
                         disabledbackground="#111a2a", disabledforeground=MUTED,
                         relief="flat", font=("Segoe UI", 10))
        entry.grid(row=row, column=1, sticky="ew", padx=(18, 0), ipady=8, pady=6)
        if disabled:
            entry.config(state="disabled")
        parent.grid_columnconfigure(1, weight=1)

    def _topper_page(self):
        if not students:
            tk.Label(self.content, text="No student records available yet.",
                     bg=BG, fg=MUTED, font=("Segoe UI", 11)).pack(pady=45)
            self._button(self.content, "+ Add Student", lambda: self.show_page("Add Student")).pack()
            return

        topper = max(students, key=lambda s: calculate_result(s["marks"])[1])
        total, percentage, grade = calculate_result(topper["marks"])
        card = tk.Frame(self.content, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=(10, 20))
        tk.Label(card, text="★  CLASS TOPPER", bg=PANEL, fg=YELLOW,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=25, pady=(24, 8))
        tk.Label(card, text=topper["name"], bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 25, "bold")).pack(anchor="w", padx=25)
        tk.Label(card, text=f"Roll Number: {topper['roll_no']}", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=25, pady=(4, 18))
        stats = tk.Frame(card, bg=PANEL)
        stats.pack(fill="x", padx=25, pady=(0, 24))
        for title, value in [
            ("TOTAL MARKS", f"{total:g} / 400"),
            ("PERCENTAGE", f"{percentage:.2f}%"),
            ("GRADE", grade),
        ]:
            box = tk.Frame(stats, bg=PANEL_ALT, padx=18, pady=14)
            box.pack(side="left", fill="x", expand=True, padx=(0, 10))
            tk.Label(box, text=title, bg=PANEL_ALT, fg=MUTED,
                     font=("Segoe UI", 8, "bold")).pack(anchor="w")
            tk.Label(box, text=value, bg=PANEL_ALT, fg=TEXT,
                     font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(5, 0))

        self._section_title(self.content, "Top student subject marks")
        for subject in SUBJECTS:
            line = tk.Frame(self.content, bg=BG)
            line.pack(fill="x", pady=5)
            tk.Label(line, text=subject, bg=BG, fg=MUTED,
                     width=16, anchor="w", font=("Segoe UI", 9)).pack(side="left")
            value = float(topper["marks"].get(subject, 0))
            bar_bg = tk.Frame(line, bg=PANEL_ALT, height=10)
            bar_bg.pack(side="left", fill="x", expand=True, padx=12)
            bar_bg.pack_propagate(False)
            tk.Frame(bar_bg, bg=ACCENT, width=0).place(relx=0, rely=0, relheight=1, relwidth=value / 100)
            tk.Label(line, text=f"{value:g}/100", bg=BG, fg=TEXT,
                     width=9, anchor="e", font=("Segoe UI", 9)).pack(side="right")

    def run(self):
        self.root.mainloop()


def main():
    load_records()
    root = tk.Tk()
    app = StudentMarksApp(root)
    app.run()


if __name__ == "__main__":
    main()
