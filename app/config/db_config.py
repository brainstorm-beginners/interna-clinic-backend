import os


def load_env(filename):
    with open(filename) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


load_env('app/config/.env')

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", default=5432)
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
