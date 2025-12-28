import subprocess
import json
import logging
import sys
import re


logger = logging.getLogger(__name__)




class PackageManager:
    """Handles package management operations."""

    @staticmethod
    def run_pip_command(cmd: list[str]) -> tuple[bool, str, str]:
        """
        Runs pip command return sucess status,stdout and stderr.


        Args:
           cmd: List of command arguments.


        Returns:
           (success,stdout,stderr)



        """

        try:
            process = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            success = (
                process.returncode == 0
            )  # set variable success to either True or False

            return success, process.stdout, process.stderr

        except FileNotFoundError as e:
            logger.error(f"Executable not found:{e}")
            return False, "", str(e)

        except OSError as e:
            logger.error(f"Os error:{e}")
            return False, "", str(e)

        except Exception as e:
            logger.error(f"Error running pip command:{e}")
            return False, "", str(e)

    @staticmethod
    def check_package_if_installed(pkg_name: str) -> tuple[bool, str]:
        """
        Check if a package is installed.

        Args:
            pkg_name: Name of the package to check

        Returns:
            Tuple: True if package is installed, False otherwise
        """

        cmd = [sys.executable, "-m", "pip", "show", pkg_name]
        

        success, stdout, stderr = PackageManager.run_pip_command(cmd)
        if success:
            return True, stdout
        else:
            return False, stderr

    @staticmethod
    def get_installed_packages() -> list[tuple[str, str]]:
        """
        Get list of all installed packages

        Returns:
            List of tuples containing (package_name ,version)

        """

        cmd = [sys.executable, "-m", "pip", "list", "--format=json"]

        success, stdout, stderr = PackageManager.run_pip_command(cmd)

        if not success:
            logger.error(f"Error getting installed packages:{stderr}")
            return []

        try:
            packages = []
            data = json.loads(stdout)
            for pkg in data:
                packages.append((pkg["name"], pkg["version"]))

            return packages

        except Exception as e:
            logger.error(f"Error parsing installed packages: {e}")
            return []

    @staticmethod
    def get_outdated_packages() -> list[tuple[str, str, str]]:
        """
        Get list of outdated packages.

        Returns:
            List of tuples containing (package_name, current_version, latest_version)
        """

        cmd = [sys.executable, "-m", "uv", "pip", "list", "--outdated", "--format=json"]

        success, stdout, stderr = PackageManager.run_pip_command(cmd)

        if not success:
            logger.error(f"Error getting outdated packages: {stderr}")
            return []

        try:
            packages = []
            data = json.loads(stdout)

            for pkg in data:
                packages.append((pkg["name"], pkg["version"], pkg["latest_version"]))

            return packages
        except json.JSONDecodeError as e:
            logger.error(f"Json parsing error:{e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing outdated packages: {e}")
            return []

    @staticmethod
    def install_package(package_name: str) -> tuple[bool, str]:
        """
        Install a new package.

        Args:
            package_name: Name of the package to install

        Returns:
            bool: True if successful, False otherwise
        """

        cmd = [sys.executable, "-m", "pip", "install", package_name]

        success, stdout, stderr = PackageManager.run_pip_command(cmd)

        if success and stdout:
            return True, stdout

        else:
            return False, stderr

    @staticmethod
    def uninstall_package(package_name) -> tuple[bool, str]:
        """
        Uninstall a package.

        Args:
            package_name: Name of the package to uninstall

        Returns:
            bool: True if successful, False otherwise
        """

        cmd = [sys.executable, "-m", "pip", "uninstall", package_name, "--yes"]

        success, stdout, stderr = PackageManager.run_pip_command(cmd)

        if success:
            return True, stdout

        else:
            return False, stderr

    @staticmethod
    def upgrade_package(package_name) -> tuple[bool, str]:
        """
        Update a package

        Args:
            package_name:Name of the package to update



        Returns:
            bool: True if succesful False otherwise



        """

        cmd_upgrade = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            package_name,
        ]

        success, stdout, stderr = PackageManager.run_pip_command(cmd_upgrade)
        if success:
            return True, stdout
        else:
            return False, stderr

    @staticmethod
    def get_packages_details(package_name):
        """
        Retrieve details about a package


        Args:
             package_name:Name of the package to get details

        Returns:
            dict: A dictionary containing package details if found else False



        """
        cmd = [sys.executable, "-m", "pip", "show", package_name]

        success, stdout, stderr = PackageManager.run_pip_command(cmd)

        if not success:
            logger.error(f"Error getting package details: {stderr}")
            return False

        details = {}

        try:
            for line in stdout.splitlines():
                key, value = line.split(":", 1)
                details[key] = value

            return details if details else False
        except ValueError as e:
            logger.error(f"Value error parsing package details:{e}")
            return False
        except Exception as e:
            logger.error(f"Error parsin package details:{e}")
            return False

    @staticmethod
    def check_package_version(package_name) -> tuple[bool,str]:
        cmd_version = [sys.executable, "-m", "pip", "index", "versions", package_name]

        # check if the latest version is already installed

        success_, stdout, stderr = PackageManager.run_pip_command(cmd_version)

        if success_:
            installed_match = re.search(r"INSTALLED:\s*(\d+\.\d+\.\d+)", stdout)
            latest_match = re.search(r"LATEST:\s*(\d+\.\d+\.\d+)", stdout)

            if not installed_match or not latest_match:
                logger.error("Could not parse version information from pip output")
                return False, "Failed to parse version information"

            installed_version = installed_match.group(1)
            latest_version = latest_match.group(1)

            if installed_version != latest_version:
                return True,""
            else:
                return False,""
