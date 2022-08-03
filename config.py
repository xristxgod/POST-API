import os
import logging


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logging.basicConfig(
    format=u"%(levelname)s:     %(filename)s line:%(lineno)d  %(message)s",
    level=logging.INFO
)


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(ROOT_DIR, 'database.db')}")
