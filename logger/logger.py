from datetime import datetime

BATCH = '[BATCH]'
DISCORD = '[DISCORD]'
BOT = '[BOT]'

class Log:
    def __init__(self):
        pass

    def info(self, type, message):
        self.logPrint(f"[INFO] - {type} - {message}")

    def warn(self, type, message):
        self.logPrint(f"[WARN] - {type} - {message}")

    def error(self, type, message):
        self.logPrint(f"[ERROR] - {type} - {message}")

    def logPrint(self, message):
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{currentTime}] - {message}"
        print(message)

log = Log()