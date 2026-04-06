from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time
from sqlalchemy import create_engine


DATABASE_URL = os.getenv("DATABASE_URL")

def wait_for_db(url, retries=10, delay=3):
    for i in range(retries):
        try:
            engine = create_engine(url)
            conn = engine.connect()
            conn.close()
            print("DB 연결 성공")
            return engine
        except Exception as e:
            print(f"DB 연결 실패 ({i+1}/{retries}) - 재시도 중...")
            time.sleep(delay)
    raise Exception("DB 연결 최종 실패")

engine = wait_for_db(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()