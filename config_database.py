# config_database.py

# Example configuration for Amazon Redshift
# Replace the placeholders with your actual credentials

REDSHIFT_CONFIG = {
    "user": "antonio_bosco",
    "password": "LT1dAsUSLvFL7cMBY7Xl",
    "host": "redshift.poligonocapital.io",
    "port": 5439,
    "database": "datalake_dw"
}

# SQLAlchemy connection string for Redshift
# Usage: from config_database import REDSHIFT_CONFIG, get_redshift_connection_string

def get_redshift_connection_string():
    cfg = REDSHIFT_CONFIG
    return f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
