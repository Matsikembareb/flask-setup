from config import Config
from app import create_app

app = create_app(config_class=Config)

