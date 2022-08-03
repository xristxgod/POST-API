from datetime import datetime


class Utils:
    @staticmethod
    def is_time(date: str) -> bool:
        data = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        if data < datetime.now():
            return False
        return True


utils = Utils
