import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(ROOT_DIR, 'database.db')}")
