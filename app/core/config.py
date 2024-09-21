import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY = os.getenv("API_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET")

settings = Settings()
