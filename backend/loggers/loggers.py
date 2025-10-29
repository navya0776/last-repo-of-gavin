import asyncio
import logging

from data.database.mongo import MongoManager


class AuditLogs(logging.Handler):
    def __init__(self, level: logging._Level = 0) -> None:
        super().__init__(level)
        self.collection = MongoManager().logs
        self.loop = asyncio.get_event_loop()

    def emit(self, record: logging.LogRecord) -> None:
        data = None
        try:
            if hasattr(record, "audit_data"):
                data = record.audit_data

            else:
                data = {
                    "message": record.getMessage(),
                    "level": record.levelname,
                    "logger": record.name,
                }

            self.loop.create_task(self.collection.insert_one(data))

        except Exception as e:
            print(f"Audit Logger Handler Error: {e}")


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[38;2;162;103;223m",  # Light Purple (underlined optional)
        logging.INFO: "\033[38;2;162;103;223m",  # Light Purple
        logging.WARNING: "\033[38;2;0;0;139m\033[1m",  # Bold Dark Blue
        logging.ERROR: "\033[38;2;255;0;0m",  # Red
        logging.CRITICAL: "\033[38;2;139;0;0m\033[1m",  # Bold Dark Red
    }

    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        reset = self.RESET

        # Customize per-level output
        if record.levelno == logging.ERROR:
            fmt = f"{color}%(levelname)s{reset}: (%(filename)s):    \033[1m%(message)s{reset}"
        elif record.levelno == logging.CRITICAL:
            fmt = f"{color}%(levelname)s{reset}: (%(filename)s):     {color}%(message)s{reset}"
        elif record.levelno == logging.DEBUG:
            fmt = f"{color}%(levelname)s{reset}:     \033[4m%(message)s{reset}"
        elif record.levelno == logging.WARNING:
            fmt = f"{color}%(levelname)s{reset}:    \033[1m%(message)s{reset}"
        else:  # INFO and default
            fmt = f"{color}%(levelname)s{reset}:     \033[37m%(message)s{reset}"

        self._style._fmt = fmt
        return super().format(record)
