import customtkinter as ctk
from tkinter import messagebox, ttk
import uuid
import random
import os

# ------------------- Admin App -------------------
class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Yesway Admin Console")
        self.geometry("1200x700")
        self.configure(bg="white")

        # === Clients with Extra Details ===
        self.clients = {
            "Ali": {
                "code": "ALI12345",
                "location": "Kochi",
                "joined": "12 Jan 2025",
                "payments": ["₹500 - Jan 2025", "₹800 - Feb 2025"],
                "computer": "Dell Inspiron 15, Windows 11"
            },
            "Amal": {
                "code": "AMAL6789",
                "location": "Calicut",
                "joined": "20 Feb 2025",
                "payments": ["₹1000 - Feb 2025"],
                "computer": "HP Elitebook, Windows 10"
            }
        }

        # === Services ===
        self.services = [
            {"client": "Ali", "task": "Fix Laptop", "status": "Pending"},
            {"client": "Amal", "task": "Install ERP", "status": "In Progress"},
        ]

        # === Orders ===
        self.orders = [
            {"type": "Computer", "client": "Rahul", "date": "25 Aug 2025"},
            {"type": "CCTV Setup", "client": "Afsal", "date": "26 Aug 2025"},
        ]

        # === Sidebar ===
        self.create_sidebar()

        # === Main Frame ===
        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.main_frame.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        self.show_dashboard()  # default

    # ---------------- Sidebar ----------------
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#FFD700")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar menu buttons
        self.menu_buttons = {}
        menu_items = {
            "Dashboard": self.show_dashboard,
            "User Creation": self.show_user_creation,
            "Services": self.show_services,
            "Orders": self.show_orders,
            "Remote Desktop": self.show_remote_desktop,
            "Quit": self.quit,
        }

        for text, cmd in menu_items.items():
            btn = ctk.CTkButton(
                self.sidebar, text=text,
                fg_color="white", text_color="black",
                hover_color="#FFFACD", command=lambda c=cmd, t=text: self.switch_menu(c, t)
            )
            btn.pack(pady=10, padx=20, fill="x")
            self.menu_buttons[text] = btn

    # ---------------- Menu Switching ----------------
    def switch_menu(self, command, text):
        for btn in self.menu_buttons.values():
            btn.configure(fg_color="white", text_color="black")

        self.menu_buttons[text].configure(fg_color="#FFA500", text_color="white")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        command()

    # ---------------- Dashboard ----------------
    def show_dashboard(self):
        lbl = ctk.CTkLabel(self.main_frame, text="📊 Admin Dashboard",
                           font=("Arial", 24, "bold"), text_color="black")
        lbl.pack(pady=20)

        stats = f"Total Clients: {len(self.clients)}\nActive Services: {len(self.services)}\nPending Orders: {len(self.orders)}"
        stat_lbl = ctk.CTkLabel(self.main_frame, text=stats,
                                font=("Arial", 16), text_color="black")
        stat_lbl.pack(pady=10)

    # ---------------- User Creation ----------------
    def show_user_creation(self):
        lbl = ctk.CTkLabel(self.main_frame, text="👤 Create New User",
                           font=("Arial", 20, "bold"), text_color="black")
        lbl.pack(pady=20)

        entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter Username",
                             width=300, height=40)
        entry.pack(pady=10)

        def create_user():
            username = entry.get().strip()
            if not username:
                messagebox.showwarning("Error", "Please enter a username")
                return
            if username in self.clients:
                messagebox.showwarning("Error", "Username already exists!")
                return

            unique_code = str(uuid.uuid4())[:8].upper()
            # Add with empty details
            self.clients[username] = {
                "code": unique_code,
                "location": "Unknown",
                "joined": "Today",
                "payments": [],
                "computer": "Not Registered"
            }
            messagebox.showinfo("Success",
                                f"User '{username}' created.\nUnique Code: {unique_code}")

        btn = ctk.CTkButton(self.main_frame, text="Generate User Code",
                            fg_color="#FFD700", text_color="black",
                            hover_color="#FFFACD", command=create_user)
        btn.pack(pady=10)

    # ---------------- Services ----------------
    def show_services(self):
        lbl = ctk.CTkLabel(self.main_frame, text="🛠 Current Services",
                           font=("Arial", 20, "bold"), text_color="black")
        lbl.pack(pady=20)

        # Treeview for services
        tree = ttk.Treeview(self.main_frame, columns=("Client", "Task", "Status"),
                            show="headings", height=10)
        tree.heading("Client", text="Client")
        tree.heading("Task", text="Task")
        tree.heading("Status", text="Status")
        tree.pack(fill="x", padx=20, pady=10)

        for idx, s in enumerate(self.services):
            tree.insert("", "end", iid=idx, values=(s["client"], s["task"], s["status"]))

        # --- Buttons for managing services ---
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        btn_frame.pack(pady=10)

        def add_service():
            self.services.append({"client": "Demo", "task": "Remote Fix",
                                  "status": random.choice(["Pending", "Delayed", "Done"])})
            self.switch_menu(self.show_services, "Services")

        def finish_service():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Error", "Please select a service to mark as Finished")
                return
            idx = int(selected[0])
            self.services[idx]["status"] = "Finished ✅"
            self.switch_menu(self.show_services, "Services")

        def delete_service():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Error", "Please select a service to delete")
                return
            idx = int(selected[0])
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this service?")
            if confirm:
                del self.services[idx]
                self.switch_menu(self.show_services, "Services")

        def show_details():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Error", "Please select a service")
                return
            idx = int(selected[0])
            client_name = self.services[idx]["client"]
            if client_name in self.clients:
                user = self.clients[client_name]
                details = f"""
Name: {client_name}
Location: {user['location']}
Joined: {user['joined']}
Computer: {user['computer']}
Payment History:
- {'\n- '.join(user['payments']) if user['payments'] else 'No Payments'}
"""
                messagebox.showinfo("User Details", details)

        add_btn = ctk.CTkButton(btn_frame, text="➕ Add Service",
                                fg_color="#FFD700", text_color="black",
                                command=add_service)
        add_btn.grid(row=0, column=0, padx=10)

        finish_btn = ctk.CTkButton(btn_frame, text="✔ Finish Service",
                                   fg_color="green", text_color="white",
                                   command=finish_service)
        finish_btn.grid(row=0, column=1, padx=10)

        delete_btn = ctk.CTkButton(btn_frame, text="🗑 Delete Service",
                                   fg_color="red", text_color="white",
                                   command=delete_service)
        delete_btn.grid(row=0, column=2, padx=10)

        details_btn = ctk.CTkButton(btn_frame, text="ℹ Show Details",
                                    fg_color="#1E90FF", text_color="white",
                                    command=show_details)
        details_btn.grid(row=0, column=3, padx=10)

    # ---------------- Orders ----------------
    def show_orders(self):
        lbl = ctk.CTkLabel(self.main_frame, text="🛒 New Orders",
                           font=("Arial", 20, "bold"), text_color="black")
        lbl.pack(pady=20)

        for order in self.orders:
            o_lbl = ctk.CTkLabel(self.main_frame,
                                 text=f"• {order['date']} - {order['client']} ordered {order['type']}",
                                 font=("Arial", 16), text_color="black")
            o_lbl.pack(anchor="w", padx=20, pady=5)

    # ---------------- Remote Desktop ----------------
    def show_remote_desktop(self):
        lbl = ctk.CTkLabel(self.main_frame, text="🖥 Remote Desktop Access",
                           font=("Arial", 20, "bold"), text_color="black")
        lbl.pack(pady=20)

        tree = ttk.Treeview(self.main_frame, columns=("Username", "Code"),
                            show="headings", height=10)
        tree.heading("Username", text="Username")
        tree.heading("Code", text="Unique Code")
        tree.pack(fill="x", padx=20, pady=10)

        for user, details in self.clients.items():
            tree.insert("", "end", values=(user, details["code"]))

        def connect_client():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Error", "Please select a client to connect")
                return

            values = tree.item(selected, "values")
            username, code = values[0], values[1]

            client_ip = "192.168.1.100"  # Replace with real client IP
            os.system(f"mstsc /v:{client_ip}")

            messagebox.showinfo("Connecting",
                                f"Attempting remote connection to {username} ({client_ip})")

        def show_details():
            selected = tree.focus()
            if not selected:
                messagebox.showwarning("Error", "Please select a client")
                return

            values = tree.item(selected, "values")
            username = values[0]
            if username in self.clients:
                user = self.clients[username]
                details = f"""
Name: {username}
Location: {user['location']}
Joined: {user['joined']}
Computer: {user['computer']}
Payment History:
- {'\n- '.join(user['payments']) if user['payments'] else 'No Payments'}
"""
                messagebox.showinfo("User Details", details)

        connect_btn = ctk.CTkButton(self.main_frame, text="🔗 Connect to Client",
                                    fg_color="#FFD700", text_color="black",
                                    command=connect_client)
        connect_btn.pack(pady=10)

        details_btn = ctk.CTkButton(self.main_frame, text="ℹ Show User Details",
                                    fg_color="#1E90FF", text_color="white",
                                    command=show_details)
        details_btn.pack(pady=10)


# ------------------- Run -------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = AdminApp()
    app.mainloop()
