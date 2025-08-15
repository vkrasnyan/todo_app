from sqlalchemy import create_engine, inspect
from pathlib import Path

from config.configs import db_settings


DATABASE_URL_SYNC = (
    "postgresql+psycopg2://"
    f"{db_settings.POSTGRES_USER}:"
    f"{db_settings.POSTGRES_PASSWORD}@"
    "localhost:"
    f"{db_settings.POSTGRES_PORT}/"
    f"{db_settings.POSTGRES_DB}"
)


output_file = Path("../docs/db_auto/schema.md")
output_file.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL_SYNC)
inspector = inspect(engine)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("# Схема базы данных\n\n")
    for table in inspector.get_table_names():
        f.write(f"## Таблица: `{table}`\n\n")
        columns = inspector.get_columns(table)
        for col in columns:
            f.write(f"- **{col['name']}** ({col['type']})\n")
        f.write("\n")
