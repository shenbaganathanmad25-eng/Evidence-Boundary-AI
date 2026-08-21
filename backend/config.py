import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "True").lower() in ("true", "1", "t")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database/evidence_boundary.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    APP_NAME: str = os.getenv("APP_NAME", "EVIDENCE BOUNDARY AI")

settings = Settings()
