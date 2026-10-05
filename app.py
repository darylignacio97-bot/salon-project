import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pathlib import Path
import json

# ============================================================
# GLAM SALON - SALON APPOINTMENT AND MANAGEMENT SYSTEM
# ============================================================

APP_DIR = Path(__file__).resolve().parent

# ============================================================
# COLORS
# ============================================================

PINK = "#E889B4"
DARK_PINK = "#B84F82"
LIGHT_PINK = "#FCEAF3"
VERY_LIGHT = "#FFF8FC"
WHITE = "#FFFFFF"
TEXT = "#3F3540"
MUTED = "#8E8490"
BORDER = "#E9D8E1"

# ============================================================
# STAFF DATA
# ============================================================

STAFF = [
    (1, "Maria Santos", "Hair Stylist", "0917-111-1111"),
    (2, "Anna Cruz", "Nail Technician", "0917-222-2222"),
    (3, "Jessica Garcia", "Hair Colorist", "0917-333-3333"),
    (4, "Sofia Reyes", "Beauty Specialist", "0917-444-4444"),
    (5, "Angela Flores", "Spa Therapist", "0917-555-5555"),
    (6, "Patricia Ramos", "Hair Stylist", "0917-666-6666"),
    (7, "Catherine Lopez", "Nail Technician", "0917-777-7777"),
    (8, "Isabella Torres", "Beauty Specialist", "0917-888-8888"),
    (9, "Michelle Aquino", "Spa Therapist", "0917-999-9999"),
    (10, "Rachel Mendoza", "Hair Stylist", "0917-000-0000"),
]

# ============================================================
# SERVICES
# ============================================================

SERVICES = {
    "Rebond": {
        "price": 1500,
        "desc": "Smooth and silky hair treatment",
        "image": "images/f7906b8e-596e-4fc4-b5e7-50a75dfef72a.jpg",
    },
    "Manicure": {
        "price": 500,
        "desc": "Beautiful and relaxing nail care",
        "image": "images/c133fd08-67a6-4b96-a337-61633bb05ba0.jpg",
    },
    "Spa": {
        "price": 800,
        "desc": "Relaxing spa and facial treatment",
        "image": "images/dcedaeb2-9d20-4578-b6f4-5222e80671f1.jpg",
    },
    "Haircut": {
        "price": 400,
        "desc": "Professional haircut and styling",
        "image": "images/8f3d5dad-b90a-4455-aa59-3f608b4ad08b.jpg",
    },
    "Hair Color": {
        "price": 1200,
        "desc": "Beautiful hair coloring service",
        "image": "images/01ac8b8f-fd86-4ddb-8679-906945f74633.jpg",
    },
}

# ============================================================
# PROMOS
# ============================================================

PROMOS = [
    (
        "Rebond",
        1800,
        1500,
        "20% OFF",
        "images/1e393630-b9b2-41e0-8529-ca2b457a7034.jpg",
    ),
    (
        "Manicure",
        600,
        500,
        "15% OFF",
        "images/a4c05bd4-bb40-4c84-b3bf-99713fe45dc2.jpg",
    ),
    (
        "Spa",
        1000,
        800,
        "15% OFF",
        "images/1b6f9182-3599-4493-97c9-a7ab52b82159.jpg",
    ),
]

# ============================================================
# APPOINTMENT HISTORY
# ============================================================

HISTORY = []
DATA_FILE = APP_DIR / "appointments.json"


def load_history():
    global HISTORY

    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                HISTORY = data
        except (json.JSONDecodeError, OSError):
            HISTORY = []


def save_history():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(HISTORY, file, indent=4, ensure_ascii=False)
    except OSError:
        messagebox.showerror(
            "Save Error",
            "The appointment history could not be saved.",
        )


def money(value):
    return f"₱{value:,.2f}"


def find_image(filename):
    """Find an image using paths relative to the project folder."""
    path = APP_DIR / filename

    if path.exists():
        return path

    # Also support a filename that already includes an images/ prefix.
    path = APP_DIR / "images" / Path(filename).name

    if path.exists():
        return path

    return None


# ============================================================
# MAIN SALON APPLICATION
# ============================================================

class SalonApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("GLAM SALON - Appointment and Management System")
        self.geometry("1250x760")
        self.minsize(1050, 650)
        self.configure(bg=VERY_LIGHT)

        self.images = {}

        self.build_layout()
        self.show_dashboard()

    # ========================================================
    # BUILD MAIN LAYOUT
    # ========================================================

    def build_layout(self):
        self.sidebar = tk.Frame(self, bg=WHITE, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=PINK, height=115)
        brand.pack(fill="x")
        brand.pack_propagate(False)

        tk.Label(
            brand,
            text="GLAM",
            bg=PINK,
            fg=WHITE,
            font=("Segoe UI", 26, "bold"),
        ).pack(pady=(20, 0))

        tk.Label(
            brand,
            text="SALON",
            bg=PINK,
            fg=WHITE,
            font=("Segoe UI", 11, "bold"),
        ).pack()

        self.nav_button("⌂  Dashboard", self.show_dashboard)
        self.nav_button("▣  Appointments", self.show_appointments)
        self.nav_button("♙  Staff", self.show_staff)
        self.nav_button("★  Promos", self.show_promos)
        self.nav_button("▤  History / Reports", self.show_history)

        tk.Frame(self.sidebar, bg=WHITE).pack(fill="both", expand=True)

        tk.Label(
            self.sidebar,
            text="Salon Hours\n10:00 AM - 8:00 PM\nMonday - Sunday",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
            justify="center",
        ).pack(pady=20)

        self.content = tk.Frame(self, bg=VERY_LIGHT)
        self.content.pack(side="right", fill="both", expand=True)

    # ========================================================
    # NAVIGATION BUTTON
    # ========================================================

    def nav_button(self, text, command):
        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            bg=WHITE,
            fg=TEXT,
            activebackground=LIGHT_PINK,
            activeforeground=DARK_PINK,
            bd=0,
            anchor="w",
            padx=25,
            pady=14,
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
        )

        button.pack(fill="x", pady=2)

    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ========================================================
    # TITLE BLOCK
    # ========================================================

    def title_block(self, title, subtitle):
        block = tk.Frame(self.content, bg=VERY_LIGHT)
        block.pack(fill="x", padx=28, pady=(20, 5))

        tk.Label(
            block,
            text=title,
            bg=VERY_LIGHT,
            fg=TEXT,
            font=("Segoe UI", 25, "bold"),
        ).pack(anchor="w")

        tk.Label(
            block,
            text=subtitle,
            bg=VERY_LIGHT,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w")

    # ========================================================
    # CARD
    # ========================================================

    def card(self, parent, bg=WHITE):
        return tk.Frame(
            parent,
            bg=bg,
            highlightbackground=BORDER,
            highlightthickness=1,
        )

    # ========================================================
    # LOAD IMAGE
    # ========================================================

    def get_image(self, filename, cache_key=None, size=(180, 120)):
        key = f"{cache_key or filename}{size}"

        if key in self.images:
            return self.images[key]

        path = find_image(filename)

        if not path:
            return None

        try:
            img = Image.open(path)
            img.thumbnail(size, Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(img)
            self.images[key] = photo

            return photo
        except Exception:
            return None

    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):
        self.clear_content()

        self.title_block(
            "Dashboard",
            "Welcome to GLAM SALON - your beauty and self-care destination",
        )

        banner_card = self.card(self.content)
        banner_card.pack(fill="x", padx=28, pady=8)

        banner = self.get_image(
            "images/59e18bfc-0816-4140-b807-38d4bdbe3c74.jpg",
            "banner",
            (1050, 220),
        )

        if banner:
            tk.Label(
                banner_card,
                image=banner,
                bg=WHITE,
            ).pack(fill="x", padx=8, pady=8)
        else:
            tk.Label(
                banner_card,
                text="WELCOME TO GLAM SALON",
                bg=LIGHT_PINK,
                fg=DARK_PINK,
                font=("Segoe UI", 24, "bold"),
                pady=45,
            ).pack(fill="x", padx=8, pady=8)

        stats = tk.Frame(self.content, bg=VERY_LIGHT)
        stats.pack(fill="x", padx=28, pady=10)

        stat_data = [
            ("Appointments", len(HISTORY), LIGHT_PINK),
            ("Services", len(SERVICES), "#F8EEF9"),
            ("Staff", len(STAFF), "#F4EFFB"),
            ("Promos", len(PROMOS), "#FFF0F5"),
        ]

        for label, value, bg in stat_data:
            c = self.card(stats, bg)
            c.pack(side="left", fill="both", expand=True, padx=5)

            tk.Label(
                c,
                text=str(value),
                bg=bg,
                fg=DARK_PINK,
                font=("Segoe UI", 25, "bold"),
            ).pack(pady=(12, 0))

            tk.Label(
                c,
                text=label,
                bg=bg,
                fg=TEXT,
                font=("Segoe UI", 11, "bold"),
            ).pack(pady=(0, 12))

        lower = tk.Frame(self.content, bg=VERY_LIGHT)
        lower.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=14,
        )

        self.service_section(lower)
        self.hours_section(lower)

    # ========================================================
    # AVAILABLE SERVICES
    # ========================================================

    def service_section(self, parent):
        left = self.card(parent)
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8),
        )

        tk.Label(
            left,
            text="✂  Available Services",
            bg=WHITE,
            fg=DARK_PINK,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", padx=18, pady=(15, 0))

        tk.Label(
            left,
            text="Pamper yourself with our 5 available services",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=20)

        canvas = tk.Canvas(left, bg=WHITE, highlightthickness=0)

        scrollbar = ttk.Scrollbar(
            left,
            orient="vertical",
            command=canvas.yview,
        )

        service_frame = tk.Frame(canvas, bg=WHITE)

        service_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            ),
        )

        canvas.create_window(
            (0, 0),
            window=service_frame,
            anchor="nw",
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=12,
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=12,
        )

        row = tk.Frame(service_frame, bg=WHITE)
        row.pack(fill="both", expand=True)

        for index, name in enumerate(SERVICES):
            info = SERVICES[name]

            c = tk.Frame(
                row,
                bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1,
            )

            c.grid(
                row=0,
                column=index,
                padx=5,
                sticky="n",
            )

            img = self.get_image(
                info["image"],
                "svc_" + name,
                (145, 100),
            )

            if img:
                tk.Label(
                    c,
                    image=img,
                    bg=WHITE,
                ).pack(pady=8)
            else:
                tk.Label(
                    c,
                    text="Image unavailable",
                    bg=LIGHT_PINK,
                    fg=MUTED,
                    width=18,
                    height=5,
                ).pack(pady=8)

            tk.Label(
                c,
                text=name,
                bg=WHITE,
                fg=DARK_PINK,
                font=("Segoe UI", 12, "bold"),
            ).pack()

            tk.Label(
                c,
                text=money(info["price"]),
                bg=WHITE,
                fg=PINK,
                font=("Segoe UI", 11, "bold"),
            ).pack(pady=2)

            tk.Label(
                c,
                text=info["desc"],
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9),
                wraplength=145,
                justify="center",
            ).pack(padx=5, pady=(0, 10))

    # ========================================================
    # SALON HOURS
    # ========================================================

    def hours_section(self, parent):
        right = self.card(parent, LIGHT_PINK)

        right.pack(
            side="right",
            fill="both",
            padx=(8, 0),
            ipadx=5,
        )

        tk.Label(
            right,
            text="◷  Salon Hours",
            bg=LIGHT_PINK,
            fg=DARK_PINK,
            font=("Segoe UI", 19, "bold"),
        ).pack(anchor="w", padx=20, pady=(18, 10))

        tk.Label(
            right,
            text="OPEN",
            bg=LIGHT_PINK,
            fg=MUTED,
            font=("Segoe UI", 10, "bold"),
        ).pack(pady=(5, 0))

        tk.Label(
            right,
            text="10:00 AM",
            bg=LIGHT_PINK,
            fg=TEXT,
            font=("Segoe UI", 20, "bold"),
        ).pack()

        tk.Label(
            right,
            text="CLOSE",
            bg=LIGHT_PINK,
            fg=MUTED,
            font=("Segoe UI", 10, "bold"),
        ).pack(pady=(12, 0))

        tk.Label(
            right,
            text="8:00 PM",
            bg=LIGHT_PINK,
            fg=TEXT,
            font=("Segoe UI", 20, "bold"),
        ).pack()

        tk.Label(
            right,
            text="Monday - Sunday\n\nWe are open and ready\nto serve you! ♡",
            bg=LIGHT_PINK,
            fg=DARK_PINK,
            font=("Segoe UI", 10),
            justify="center",
        ).pack(pady=15)

    # ========================================================
    # APPOINTMENTS
    # ========================================================

    def show_appointments(self):
        self.clear_content()

        self.title_block(
            "Appointments",
            "Create a new salon appointment",
        )

        outer = self.card(self.content)
        outer.pack(fill="x", padx=120, pady=10)

        form = tk.Frame(outer, bg=WHITE)
        form.pack(padx=35, pady=25)

        fields = {}

        field_names = [
            "Customer Name",
            "Contact",
            "Date",
            "Time",
        ]

        for i, label in enumerate(field_names):
            tk.Label(
                form,
                text=label,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 10, "bold"),
            ).grid(
                row=i,
                column=0,
                sticky="w",
                pady=7,
                padx=(0, 15),
            )

            entry = tk.Entry(
                form,
                width=32,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1,
            )

            entry.grid(row=i, column=1, pady=7)
            fields[label] = entry

        tk.Label(
            form,
            text="Service",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=7,
        )

        service = ttk.Combobox(
            form,
            values=list(SERVICES.keys()),
            state="readonly",
            width=29,
        )

        service.set("Rebond")
        service.grid(row=4, column=1, pady=7)

        tk.Label(
            form,
            text="Staff",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold"),
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=7,
        )

        staff = ttk.Combobox(
            form,
            values=[x[1] for x in STAFF],
            state="readonly",
            width=29,
        )

        staff.set("Maria Santos")
        staff.grid(row=5, column=1, pady=7)

        def book():
            customer = fields["Customer Name"].get().strip()
            contact = fields["Contact"].get().strip()
            date = fields["Date"].get().strip()
            time = fields["Time"].get().strip()
            svc = service.get()
            emp = staff.get()

            if not all([customer, contact, date, time, svc, emp]):
                messagebox.showwarning(
                    "Missing Information",
                    "Please complete all appointment fields.",
                )
                return

            HISTORY.append(
                {
                    "customer": customer,
                    "contact": contact,
                    "date": date,
                    "time": time,
                    "service": svc,
                    "staff": emp,
                    "price": SERVICES[svc]["price"],
                    "status": "Booked",
                }
            )

            save_history()

            messagebox.showinfo(
                "Appointment Saved",
                "Appointment successfully booked!",
            )

            self.show_history()

        tk.Button(
            form,
            text="BOOK APPOINTMENT",
            command=book,
            bg="#C98AB0",
            fg=WHITE,
            activebackground=DARK_PINK,
            activeforeground=WHITE,
            bd=0,
            font=("Segoe UI", 11, "bold"),
            padx=35,
            pady=10,
            cursor="hand2",
        ).grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(20, 5),
        )

    # ========================================================
    # STAFF
    # ========================================================

    def show_staff(self):
        self.clear_content()

        self.title_block(
            "Staff Management",
            "Salon staff information",
        )

        box = self.card(self.content)

        box.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=8,
        )

        cols = ("ID", "Name", "Position", "Contact")

        tree = ttk.Treeview(
            box,
            columns=cols,
            show="headings",
        )

        widths = (70, 260, 220, 220)

        for col, width in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(
                col,
                width=width,
                anchor="center",
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12,
        )

        for row in STAFF:
            tree.insert("", "end", values=row)

    # ========================================================
    # PROMOS
    # ========================================================

    def show_promos(self):
        self.clear_content()

        self.title_block(
            "Promos",
            "Current GLAM SALON promotions",
        )

        row = tk.Frame(self.content, bg=VERY_LIGHT)

        row.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=10,
        )

        for name, old, new, discount, image_name in PROMOS:
            c = self.card(row, WHITE)

            c.pack(
                side="left",
                fill="both",
                expand=True,
                padx=8,
                pady=5,
            )

            tk.Label(
                c,
                text=name.upper() + " PROMO",
                bg=WHITE,
                fg=DARK_PINK,
                font=("Segoe UI", 15, "bold"),
            ).pack(pady=(18, 10))

            img = self.get_image(
                image_name,
                "promo_" + name,
                (250, 180),
            )

            if img:
                tk.Label(
                    c,
                    image=img,
                    bg=WHITE,
                ).pack(pady=3)
            else:
                tk.Label(
                    c,
                    text="Promo image unavailable",
                    bg=LIGHT_PINK,
                    fg=MUTED,
                    width=25,
                    height=7,
                ).pack(pady=3)

            tk.Label(
                c,
                text=discount,
                bg="#F24E89",
                fg=WHITE,
                font=("Segoe UI", 10, "bold"),
                padx=12,
                pady=4,
            ).pack(pady=8)

            tk.Label(
                c,
                text=money(old),
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 10),
            ).pack()

            tk.Label(
                c,
                text=money(new),
                bg=WHITE,
                fg=PINK,
                font=("Segoe UI", 18, "bold"),
            ).pack()

            tk.Label(
                c,
                text=f"Promo price • {name}",
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 10),
            ).pack(pady=(3, 20))

    # ========================================================
    # HISTORY / REPORTS
    # ========================================================

    def show_history(self):
        self.clear_content()

        self.title_block(
            "History / Reports",
            "Previous salon appointment records",
        )

        box = self.card(self.content)

        box.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=8,
        )

        cols = (
            "Customer",
            "Contact",
            "Date",
            "Time",
            "Service",
            "Staff",
            "Price",
            "Status",
        )

        tree = ttk.Treeview(
            box,
            columns=cols,
            show="headings",
        )

        widths = (
            170,
            130,
            100,
            95,
            120,
            150,
            90,
            90,
        )

        for col, width in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(
                col,
                width=width,
                anchor="center",
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12,
        )

        for r in HISTORY:
            tree.insert(
                "",
                "end",
                values=(
                    r.get("customer", ""),
                    r.get("contact", ""),
                    r.get("date", ""),
                    r.get("time", ""),
                    r.get("service", ""),
                    r.get("staff", ""),
                    money(r.get("price", 0)),
                    r.get("status", ""),
                ),
            )


# ============================================================
# ADMIN LOGIN WINDOW
# ============================================================

class LoginWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("GLAM SALON - Admin Login")
        self.geometry("450x500")
        self.resizable(False, False)
        self.configure(bg=VERY_LIGHT)

        self.update_idletasks()

        width = 450
        height = 500

        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(
            self,
            text="GLAM SALON",
            bg=PINK,
            fg=WHITE,
            font=("Segoe UI", 26, "bold"),
            pady=20,
        ).pack(fill="x")

        tk.Label(
            self,
            text="Login",
            bg=VERY_LIGHT,
            fg=TEXT,
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=(30, 5))

        tk.Label(
            self,
            text="Salon Appointment and Management System",
            bg=VERY_LIGHT,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack()

        form = tk.Frame(
            self,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )

        form.pack(
            padx=45,
            pady=25,
            fill="x",
        )

        tk.Label(
            form,
            text="Username",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold"),
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5),
        )

        self.user = tk.Entry(
            form,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
        )

        self.user.pack(fill="x", padx=25)

        tk.Label(
            form,
            text="Password",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold"),
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5),
        )

        self.password = tk.Entry(
            form,
            show="*",
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
        )

        self.password.pack(fill="x", padx=25)

        tk.Button(
            form,
            text="LOGIN",
            command=self.login,
            bg=PINK,
            fg=WHITE,
            activebackground=DARK_PINK,
            activeforeground=WHITE,
            bd=0,
            font=("Segoe UI", 11, "bold"),
            padx=30,
            pady=9,
            cursor="hand2",
        ).pack(pady=22)

        tk.Label(
            self,
            text="GLAM SALON • Admin Access",
            bg=VERY_LIGHT,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack()

        self.user.focus()

        self.bind(
            "<Return>",
            lambda event: self.login(),
        )

    # ========================================================
    # LOGIN FUNCTION
    # ========================================================

    def login(self):
        username = self.user.get().strip()
        password = self.password.get()

        if username == "admin" and password == "admin123":
            self.destroy()

            app = SalonApp()
            app.mainloop()
        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password.",
            )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    load_history()
    LoginWindow().mainloop()
