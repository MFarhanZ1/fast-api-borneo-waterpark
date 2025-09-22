from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ganti dengan kredensial Anda
# DB_USER = "wyscrtdd_farhan"
# DB_PASS = "2H1RkTMWxBUdIKcKs2tKZNvDoJNZ052O4tUW7VpuIn8srZGUEF2H1RkTMWxBUdIKcKs2tKZNvDoJNZ052O4tUW7VpuIn8srZGUEF"
# DB_HOST = "localhost" # atau IP server database Anda
# DB_NAME = "wyscrtdd_db_borneo_waterpark"

DB_USER = "root"
DB_PASS = ""
DB_HOST = "localhost" # atau IP server database Anda
DB_NAME = "db_borneo_waterpark"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency untuk mendapatkan sesi database di setiap request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()