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

Clone the repository:

```sh
git clone https://github.com/mathias-ted/PythonPackageManager
```

Install in editable mode:

```sh
uv pip install -e .
```

<<<<<<< HEAD
Run Application

```sh
uv run pkgr
```
=======
## ▶️ Usage

Run the application:

```sh
uv run pkgr
```

**Note:** `pkgr` detects its execution context automatically:
- If run inside an activated virtual environment, it manages packages for that environment.
- If run in the global/system environment, it manages global packages instead.
>>>>>>> 47a12d6 (docs: fix README formatting, install command, and usage clarity)
