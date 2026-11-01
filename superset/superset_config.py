import os

# Local/class use only. Override SUPERSET_SECRET_KEY in a .env file for anything else.
SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

# Superset's own metadata (users, charts, dashboards) lives in a SQLite file in the named volume
SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"

# UI in Portuguese by default
BABEL_DEFAULT_LOCALE = "pt_BR"
LANGUAGES = {
    "pt_BR": {"flag": "br", "name": "Português"},
    "en": {"flag": "us", "name": "English"},
}
