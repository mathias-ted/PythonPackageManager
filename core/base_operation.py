from core.package_manager import PackageManager


class Operations:
    def __init__(
        self,
        name,
        operation,
        update_status_ui,
        show_info_win,
        show_err_win,
        update_status,
    ):
        self.name = name
        self.operation = operation
        self.update_status = update_status
        self.update_status_ui = update_status_ui
        self.show_info_win = show_info_win
        self.show_err_win = show_err_win
        self.is_package_installed()

    def is_package_installed(self):
        self.update_status_ui(f"Checking if {self.name} is installed....", "loading")
        installed, _ = PackageManager.check_package_if_installed(self.name)
        if self.operation == "uninstall" or self.operation == "upgrade":
            if installed:
                self.run_operations_()

            else:
                self.update_status_ui(f"{self.name} not found")
                self.show_info_win(f"{self.name} not found")

        elif installed:
            self.update_status_ui(f"'{self.name}' is already installed")
            self.show_info_win(f"'{self.name}' is already installed")
        else:
            self.run_operations_()

    def run_operations_(self):
        if self.operation == "install":
            self.update_status_ui(
                f"{self.operation.capitalize()}ing {self.name}....", "loading"
            )
            success, message = PackageManager.install_package(self.name)
            self.sync_status(success, message)
        if self.operation == "upgrade":
            self.update_status_ui(
                f"Checking if {self.name} is the latest version", "loading"
            )
            state, message_ = PackageManager.check_package_version(self.name)
            if state:
                self.update_status_ui(f"Upgrading {self.name} ", "loading")
                success, message = PackageManager.upgrade_package(self.name)
                self.sync_status(success, message)
            else:
                self.update_status_ui("You have the latest version", "loading")
                self.show_info_win("You have the latest version")

        if self.operation == "uninstall":
            self.update_status_ui(
                f"{self.operation.capitalize()}ing {self.name}....", "loading"
            )
            success, message = PackageManager.uninstall_package(self.name)
            self.sync_status(success, message)

    def sync_status(self, success, message):
        if success:
            self.update_status_ui(message, "success")
            self.show_info_win(message)
        else:
            self.update_status_ui(message, "error")
            self.show_err_win(f"Failed to {self.operation}'{self.name}'\n{message}")
        
        self.update_status("Ready to manage packages", "info")

