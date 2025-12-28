import logging

from gui.main_window import PackageManagerApp

from tkinter import messagebox


# configure logging

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s - %(levelname)s - %(message)s    "),
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),  # show in a console
    ],
)

logger = logging.getLogger(__name__)


def main():
    try:
        app = PackageManagerApp()

        app.mainloop()

    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")

        messagebox.showerror(
            "❌ Critical Error", f"Application failed to start: {str(e)}"
        )


if __name__ == "__main__":
    logger.info("Application started")
    main()
