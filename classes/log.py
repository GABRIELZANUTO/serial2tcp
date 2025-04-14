import os
from datetime import datetime

class LogManager:
    def __init__(self, log_dir="log", base_filename="log", max_size_mb=2):
        self.log_dir = log_dir
        self.base_filename = base_filename
        self.max_size = max_size_mb * 1024 * 1024 
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        os.makedirs(self.log_dir, exist_ok=True)
        self.current_index = self._get_last_log_index()

    def _get_log_files_for_today(self):
        files = os.listdir(self.log_dir)
        return [f for f in files if f.startswith(f"{self.base_filename}_{self.current_date}_")]

    def _get_last_log_index(self):
        today_logs = self._get_log_files_for_today()
        indices = []
        for name in today_logs:
            parts = name.replace(".log", "").split("_")
            if len(parts) >= 3 and parts[2].isdigit():
                indices.append(int(parts[2]))
        return max(indices, default=1)

    def _get_current_log_path(self):
        return os.path.join(
            self.log_dir,
            f"{self.base_filename}_{self.current_date}_{self.current_index}.log"
        )

    def _rotate_log_if_needed(self):
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.current_date:
            # Se mudou o dia, reinicia o índice
            self.current_date = today
            self.current_index = 1
        else:
            path = self._get_current_log_path()
            if os.path.exists(path) and os.path.getsize(path) >= self.max_size:
                self.current_index += 1

    def write(self, message: str):
        self._rotate_log_if_needed()
        timestamp = datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")
        path = self._get_current_log_path()
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {message.strip()}\n")
