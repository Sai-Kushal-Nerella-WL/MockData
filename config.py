"""
Configuration module for database connection and data generation settings.
Loads environment variables from .env file.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for database and data generation settings."""
    
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'citi_db')
    
    RANDOM_SEED = int(os.getenv('RANDOM_SEED', 42))
    NUM_CUSTOMERS = int(os.getenv('NUM_CUSTOMERS', 500))
    NUM_EMPLOYEES = int(os.getenv('NUM_EMPLOYEES', 500))
    NUM_BRANCHES = int(os.getenv('NUM_BRANCHES', 500))
    NUM_ACCOUNTS = int(os.getenv('NUM_ACCOUNTS', 500))
    
    @classmethod
    def get_database_url(cls):
        """Generate SQLAlchemy database URL."""
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
