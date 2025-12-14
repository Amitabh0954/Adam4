"""
Configuration settings.
"""

import os

class Config:
    DEBUG = os.getenv('DEBUG', True)
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME', 'session')
