import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    TEMPLATES_AUTO_RELOAD = True
