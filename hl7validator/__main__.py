"""Main entry point for hl7validator package."""

from hl7validator import app
import os
import logging
from logging.handlers import RotatingFileHandler


def main():
    """Main entry point for the application."""
    if not app.debug:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/message_validation.log", maxBytes=1_000_000, backupCount=20
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)

    app.run()


if __name__ == "__main__":
    main()
