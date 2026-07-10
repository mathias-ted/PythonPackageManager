# PythonPackageManager

A lightweight GUI-based Python package manager that allows you to install, update, and uninstall Python packages.

## 🚀 Features

- 📦 Install Python packages
- 🔄 Update installed packages
- ❌ Uninstall packages
- 🖥️ Simple GUI interface

<img width="514" height="693" alt="sample 3" src="https://github.com/user-attachments/assets/8a9bbd0f-e3e4-4467-9073-a0f262f934a9" />

<img width="744" height="576" alt="sample 2" src="https://github.com/user-attachments/assets/1de5de8e-209f-472d-949e-7dd0d45ef9f7" />
<img width="744" height="583" alt="sample 1" src="https://github.com/user-attachments/assets/85496f94-1a05-4b54-a47a-a779d4d39e60" />

## 📦 Installing

**Prerequisite:** `pkgr` requires [`uv`](https://docs.astral.sh/uv/) to already be installed on your system,This applies whether you're running `pkgr` inside a virtual environment or globally — either way, `uv` needs to be reachable on your PATH. See the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it yet.

Install `pkgr` as a CLI tool directly from GitHub:

```sh
uv tool install git+https://github.com/mathias-ted/PythonPackageManager
```

This installs `pkgr` in an isolated environment managed by `uv` and makes it available globally — no manual cloning or virtual environment activation needed.

### Developing / contributing

If you want to modify the source instead:

```sh
git clone https://github.com/mathias-ted/PythonPackageManager
cd PythonPackageManager
uv run pkgr
```

`uv run` automatically creates a `.venv`, installs the project in editable mode, and resolves dependencies — no separate install step required.

## ▶️ Usage

Run the application:

```sh
pkgr
```

**Note:** `pkgr` detects its execution context automatically:
- If run inside an activated virtual environment, it manages packages for that environment.
- If run in the global/system environment, it manages global packages instead.