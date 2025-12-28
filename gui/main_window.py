import customtkinter
from gui.packages_window import PackageWindow
from core.package_manager import PackageManager

from tkinter import messagebox

import threading

import functools
from core.base_operation import Operations


class PackageManagerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.setup_app()

        self.setup_ui()

    def setup_app(self):
        """initialize application settings"""
        # customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")

        self.title("Python Package Manager")
        self.geometry("520x700")
        self.minsize(500, 650)

        self.configure(fg_color=("#f0f0f0", "#0a0a0a"))

    def setup_ui(self):
        self.main_frame = customtkinter.CTkFrame(
            self,
            fg_color=("#f8f9fa", "#1a1a1a"),
            corner_radius=15,
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.setup_header()

        self.setup_action_buttons()

        self.setup_status_action()

    def setup_header(self):
        header_frame = customtkinter.CTkFrame(
            self.main_frame,
            fg_color="transparent",
        )

        header_frame.pack(fill="x", pady=(20, 30))

        # main title
        self.title_label = customtkinter.CTkLabel(
            header_frame,
            text="🐍 Python Package Manager",
            font=customtkinter.CTkFont(size=26, weight="bold"),
            text_color=("#2c3e50", "#3498db"),
        )
        self.title_label.pack(pady=(0, 5))

        # subtitle
        self.subtitle_label = customtkinter.CTkLabel(
            header_frame,
            text="Manage your python packages",
            font=customtkinter.CTkFont(size=13),
            text_color=("#7f8c8d", "#95a5a6"),
        )
        self.subtitle_label.pack()

    def create_buttons(self, parent, text, command, fg_color, hover_color):
        btn = customtkinter.CTkButton(
            parent,
            text=text,
            command=command,
            corner_radius=12,
            height=45,
            font=customtkinter.CTkFont(size=15, weight="bold"),
            fg_color=fg_color,
            hover_color=hover_color,
            border_width=0,
        )
        return btn

    def setup_action_buttons(self):
        # Buttons container

        buttons_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")

        buttons_frame.pack(fill="x", padx=20)

        primary_buttons = [
            (
                "📦 Install Package",
                functools.partial(self.show_input_dialog, "install"),
                "#27ae60",
                "#2ecc71",
            ),
            (
                "📋 View Packages",
                functools.partial(self.show_installed_packages_window),
                "#3498db",
                "#5dade2",
            ),
            (
                "⬆️ Upgrade Package",
                functools.partial(self.show_input_dialog, "upgrade"),
                "#f39c12",
                "#e67e22",
            ),
            (
                "⚠️ Check Outdated",
                functools.partial(self.show_outdated_package_window),
                "#e74c3c",
                "#c0392b",
            ),
            (
                "🗑️ Uninstall Package",
                functools.partial(self.show_input_dialog, "uninstall"),
                "#95a5a6",
                "#7f8c8d",
            ),
        ]

        for text, command, fg_color, hover_color in primary_buttons:
            button = self.create_buttons(
                buttons_frame,
                text=text,
                command=command,
                fg_color=fg_color,
                hover_color=hover_color,
            )

            button.pack(pady=8, fill="x")

    def setup_status_action(self):
        """a status icon to show the current action"""
        status_frame = customtkinter.CTkFrame(
            self.main_frame,
            fg_color=("#ecf0f1", "#2c3e50"),
            corner_radius=10,
            height=60,
        )
        status_frame.pack(fill="x", padx=20, pady=(30, 20))

        status_frame.pack_propagate(False)

        # status icon and text

        status_container = customtkinter.CTkFrame(status_frame, fg_color="transparent")

        status_container.pack(expand=True)

        self.status_icon = customtkinter.CTkLabel(
            status_container,
            text="⚡",
            font=customtkinter.CTkFont(size=16),
        )
        self.status_icon.pack(side="left", padx=(10, 5))

        self.status_label = customtkinter.CTkLabel(
            status_container,
            text="Ready to manage packages",
            font=customtkinter.CTkFont(size=13, weight="bold"),
        )
        self.status_label.pack(side="left")

    def update_status(self, message, status_type="info"):
        """Update the status label"""

        status_icons = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "loading": "⏳",
        }

        icon = status_icons.get(status_type, "⚡")

        self.status_icon.configure(text=icon)
        self.status_label.configure(text=message)

        self.update()

    def show_input_dialog(self, operation):
        """show input dialog for package operations"""

        dialog_titles = {
            "install": " 📦 Install New Package",
            "upgrade": " ⬆ Upgrade Package",
            "uninstall": " 🗑️ Uninstall Package",
        }

        dialog = customtkinter.CTkInputDialog(
            text=f"Enter the package name to {operation}:",
            title=dialog_titles.get(operation, "package operation"),
        )

        package_name = dialog.get_input()

        if package_name:
            self.execute_package_operation(operation, package_name.strip())

    def execute_package_operation(self, operation, package_name):
        def run_operation():
            try:
                Operations(
                    package_name,
                    operation,
                    self.update_status_ui,
                    self.show_info_win,
                    self.show_err_win,
                    self.update_status,
                )
            except Exception as e:
                print(e)

        threading.Thread(target=run_operation, daemon=True).start()

    def show_info_win(self, message):
        # run command in the main thread using self.after
        self.after(0, lambda: messagebox.showinfo("Info", message))

    def show_err_win(self, message):
        self.after(0, lambda: messagebox.showerror("Error", message))

    def update_status_ui(self, message, status_type="info"):
        self.after(0, lambda: self.update_status(message, status_type))

    def show_installed_packages_window(self):
        """Display a window with installed packages"""

        try:
            self.update_status("Loading installed packages....", "loading")

            packages = PackageManager.get_installed_packages()

            if not packages:
                messagebox.showinfo(
                    "⚠️ Warning", "No packages found or failed to retrieve package list"
                )
                self.update_status("Ready to manage packages", "info")

                return

            PackageWindow(
                parent=self,
                window_type="installed",
                packages=packages,
                columns=["#", "package_name", "version"],
                title="📋 Installed Packages",
            )
            self.update_status(f"Found {len(packages)} installed packages", "info")

        except Exception as e:
            print(e)

    def show_outdated_package_window(self):
        """Display a window with outdated packages"""

        def load_outdated():
            try:
                self.update_status("Checking for outdated packages.....", "loading")
                packages = PackageManager.get_outdated_packages()

                if not packages:
                    self.update_status("All packages are up to date! ", "success")
                    messagebox.showinfo("ℹ️ Info", "All packages are up to date!")

                    return

                PackageWindow(
                    window_type="outdated",
                    packages=packages,
                    parent=self,
                    columns=["#", "Package Name", "Current Version", "Latest Version"],
                    title="⚠️ Outdated Packages",
                )

                self.update_status(
                    f"Found {len(packages)} outdated packages", "warning"
                )
            except Exception as e:
                error_msg = f"Failed to check outdated packages: {str(e)}"
                messagebox.showerror("❌ Error", error_msg)

                self.update_status("Failed to check updates", "error")

        load_outdated()
