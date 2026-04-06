from fastapi import FastAPI
from db import Base, engine, SessionLocal
from models import Product
from redis_client import redis_client
import json
from contextlib import asynccontextmanager


# DB 세션
def get_db():
    return SessionLocal()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = get_db()
    if db.query(Product).count() == 0:
        db.add_all([
            Product(name="apple", price=1000),
            Product(name="banana", price=2000),
        ])
        db.commit()
    db.close()
    yield
    

app = FastAPI(lifespan=lifespan)

# 초기 데이터 넣기
# @app.on_event("startup")
# def seed_data():
#     db = get_db()
#     if db.query(Product).count() == 0:
#         db.add_all([
#             Product(name="apple", price=1000),
#             Product(name="banana", price=2000),
#         ])
#         db.commit()
#     db.close()

# 🔥 캐싱 적용 API
@app.get("/products")
def get_products():
    # 1. Redis 조회
    cached = redis_client.get("products")

    if cached:
        return {
            "source": "redis",
            "data": json.loads(cached)
        }

    # 2. DB 조회
    db = get_db()
    products = db.query(Product).all()

    result = [
        {"id": p.id, "name": p.name, "price": p.price}
        for p in products
    ]

    # 3. Redis 저장 (60초 캐싱)
    redis_client.set("products", json.dumps(result), ex=60)

    return {
        "source": "db",
        "data": result
    }