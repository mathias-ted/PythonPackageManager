import site
import os
import subprocess
import threading
import platform


from customtkinter import (
    StringVar,
    CTkToplevel,
    CTkEntry,
    CTkFont,
    CTkLabel,
    CTkTextbox,
    CTkButton,
    CTkFrame,
)
from tkinter import ttk


from tkinter import messagebox, Menu


from core.package_manager import PackageManager


class PackageWindow:
    def __init__(
        self,
        window_type: str,
        packages,
        parent,
        columns: list[str],
        title: str,
    ):
        self.parent = parent
        self.packages = packages

        self.columns = columns
        self.window_type = window_type
        self.title = title

        # search variables
        self.search_var = StringVar()
        self.search_var.trace_add("write", self.filter_packages)

        self.package_folder = self.get_packages_dir()

        self.create_window()

    def create_window(self):
        """Create a new window for handle packages"""

        self.window = CTkToplevel(self.parent)

        self.window.title(self.title)

        self.window.geometry("750x550")

        self.window.transient(self.parent)

        self.window.grab_set()  # Grab all events
        self.window.focus_set()  # Focus on new window

        self.window.configure(fg_color=("#f8f9fa", "#1a1a1a"))

        # Main container frame

        main_container = CTkFrame(self.window, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Header
        self.setup_header(main_container)

        # Packages list

        self.setup_packages_list(main_container)

        self._on_window_close()

    def update_main_window_status(self):
        self.parent.update_status("Ready to manage packages", status_type="")
        self.window.destroy()

    def _on_window_close(self):
        self.window.protocol("WM_DELETE_WINDOW", self.update_main_window_status)

    def setup_header(self, parent):
        header_frame = CTkFrame(parent, fg_color=("#ecf0f1", "#2c3e50"))
        header_frame.pack(fill="x", pady=(0, 15))

        # search section
        search_container = CTkFrame(header_frame, fg_color="transparent")
        search_container.pack(fill="x", padx=15, pady=15)

        search_label = CTkLabel(
            search_container,
            text="🔍 Search:",
            font=CTkFont(size=14, weight="bold"),
        )

        search_label.pack(side="left", padx=(0, 10))

        search_entry = CTkEntry(
            search_container,
            textvariable=self.search_var,
            placeholder_text="Type package name to filter",
            corner_radius=8,
            height=35,
        )

        search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        # Refresh Button

        refresh_button = CTkButton(
            search_container,
            text="🔄 Refresh",
            width=100,
            height=35,
            corner_radius=8,
            fg_color="#3498db",
            hover_color="#2980b9",
            command=lambda: self.refresh_package(),
        )

        refresh_button.pack(side="right")

    def show_package_details_window(self, details):
        window = CTkToplevel(self.window)

        window.title("Package details")

        window.geometry("600x400")

        window.grab_set()
        window.focus_set()

        window.transient(self.window)

        txt_box = CTkTextbox(
            window, width=580, height=380, fg_color=("#ecf0f1", "#2c3e50")
        )

        txt_box.pack(fill="both", expand=True, padx=10, pady=10)

        for key, value in details.items():
            txt_box.insert("end", f"{key}:{value}\n\n")

        txt_box.configure(state="disabled")

    def get_packages_dir(self):
        try:
            return site.getsitepackages()[1]

        except (IndexError, AttributeError):
            messagebox.showerror("Could not determine package directory")

            return ""

    def setup_packages_list(self, parent):
        # Treeview container

        tree_container = CTkFrame(
            parent, fg_color=("#ffffff", "#2c3e50"), corner_radius=10
        )
        tree_container.pack(fill="both", expand=True)

        # Treeview heading style

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#34495e",
            foreground="#ecf0f1",
            fieldbackground="#34495e",
            borderwidth=0,
            font=("Segoe UI", 10),
        )

        style.configure(
            "Treeview.Heading",
            background="#2c3e50",
            foreground="#ecf0f1",
            font=("Segoe UI", 10, "bold"),
        )

        # create the treeview
        self.treeview = ttk.Treeview(
            tree_container, columns=self.columns, show="headings", style="Treeview"
        )

        for i, col in enumerate(self.columns):
            self.treeview.heading(col, text=col)

            self.treeview.column(col, width=50, anchor="center")

            if i == 0:
                self.treeview.column(col, width=50, anchor="center")
            else:
                self.treeview.column(col, width=100, anchor="center")

        # scrollbar

        scrollbar = ttk.Scrollbar(
            tree_container,
            orient="vertical",
            command=self.treeview.yview,
        )

        self.treeview.configure(yscrollcommand=scrollbar.set)

        self.treeview.pack(side="left", fill="both", padx=10, pady=10, expand=True)
        scrollbar.pack(side="left", fill="y", pady=10)

        # add items to treeview

        self.populate_treeview(self.packages)

        self.treeview.bind("<Button-3>", self.show_context_menu)

    def populate_treeview(self, packages: list[tuple]):
        # clear existing items

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # insert packages

        for i, pkg in enumerate(packages, 1):
            self.treeview.insert(parent="", index="end", values=(i, *pkg))

    def filter_packages(self, *_):
        """Filter packages based on search input"""

        query = self.search_var.get().lower().strip()

        self.filtered_packages = [pkg for pkg in self.packages if query in pkg[0]]

        self.populate_treeview(self.filtered_packages)

    def show_context_menu(self, event):
        row = self.treeview.identify_row(event.y)
        if not row:
            return
        self.treeview.selection_set(row)

        menu = Menu(self.window, tearoff=0)
        menu.add_command(
            label="Copy Name",
            command=self.copy_package_name,
        )
        menu.add_command(
            label="Open Path",
            command=self.open_package_location,
        )
        menu.add_command(
            label="Uninstall",
            command=self.uninstall_from_menu,
        )
        menu.add_command(
            label="About",
            command=self.show_package_details,
        )

        if self.window_type == "outdated":
            menu.add_command(label="Update", command=self.update_from_menu)

        menu.post(event.x_root, event.y_root)

    def get_selected_package(self):
        selection = self.treeview.selection()[0]

        if not selection:
            messagebox.showerror("❌ Error", "No package selected")
            return None

        return self.treeview.item(selection)["values"][1]

    def copy_package_name(self):
        """Copy selected item to clipboard"""

        name = self.get_selected_package()
        if name:
            self.window.clipboard_clear()

            self.window.clipboard_append(name)

            messagebox.showinfo(
                "📋 Copied", f"Package name '{name}' copied to clipboard"
            )

    def open_package_location(self):
        """Open package location in file explorer"""

        name = self.get_selected_package()

        if not name or not self.package_folder:
            return

        folder_path = name.replace("-", "_") if "-" in name else name
        full_path = os.path.join(self.package_folder, folder_path)

        if not os.path.exists(full_path):
            messagebox.showerror(
                "⚠️ Warning", f"Package directory not found:\n{full_path}"
            )
            return

        try:
            if platform.system() == "Windows":  # windows
                subprocess.Popen(f"explorer /select , {full_path}")
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-R", full_path])
            elif platform.system() == "Linux":
                subprocess.Popen(["xdg-open", full_path])

        except Exception as e:
            messagebox.showerror(
                "❌ Error", f"Failed to open package location: {str(e)}"
            )

    def uninstall_from_menu(self):
        """Uninstall package from context menu"""

        name = self.get_selected_package()

        if not name:
            return

        if messagebox.askyesno(
            "🗑️ Confirm Uninstall",
            f"Are you sure you want to uninstall '{name}'?",
        ):
            try:
                self.parent.update_status(f"Uninstalling {name}", "loading")
                success, msg = PackageManager.uninstall_package(name)

                if success:
                    self.parent.update_status(
                        f"package {name} uninstalled successfully", "success"
                    )
                else:
                    self.parent.update_status(
                        f"Failed to uninstall {name}:{msg}", "error"
                    )
            except Exception as e:
                self.parent.update_status(
                    f"Error uninstalling {name}: {str(e)}", "error"
                )

    def show_package_details(self):
        name = self.get_selected_package()

        if not name:
            return

        package_details = PackageManager.get_packages_details(name)

        if not package_details:
            messagebox.showerror("❌ Error", "Failed to get package details")
            return

        self.show_package_details_window(package_details)

    def update_from_menu(self):
        name = self.get_selected_package()

        if not name:
            return

        if messagebox.askyesno(
            "⬆️ Confirm Upgrade",
            f"Are you sure you want to upgrade '{name}'to the latest version?",
        ):
            success, message = PackageManager.upgrade_package(name)
            if success:
                messagebox.showinfo("✅ Success", message)
            else:
                messagebox.showerror("❌ Error", message)

    def refresh_package(self):
        """Refresh package list"""

        def refresh():
            try:
                if self.window_type == "installed":
                    self.packages = PackageManager.get_installed_packages()

                elif self.window_type == "outdated":
                    self.packages = PackageManager.get_outdated_packages()

                    if not self.packages:
                        messagebox.showinfo(
                            "ℹ️ Info", "All packages are now up to date!"
                        )
                        self.window.destroy()
                        return

                # update packages and refresh display

                self.filter_packages()

                self.window.after(
                    0,
                    lambda: messagebox.showinfo(
                        "✅ Success",
                        f"{self.window_type.capitalize()} packages refreshed!",
                    ),
                )

            except Exception as e:
                error_msg = f"Failed to refresh package list: {str(e)}"

                self.window.after(
                    0, lambda: messagebox.showerror("❌ Error", error_msg)
                )

        threading.Thread(target=refresh, daemon=True).start()
