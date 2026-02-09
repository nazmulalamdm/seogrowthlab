from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ডকার এনভায়রনমেন্টের জন্য DATABASE_URL
# এখানে postgresql+psycopg ব্যবহার করা হয়েছে যাতে Psycopg 3 ড্রাইভারটি কাজ করে
# এবং localhost এর বদলে 'db' ব্যবহার করা হয়েছে যাতে ডকার কন্টেইনার ডাটাবেজকে খুঁজে পায়
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg://postgres:123456@db:5432/seo_growth_db"
)

# কানেকশন ইঞ্জিন তৈরি (প্রোডাকশন প্যারামিটারসহ)
engine = create_engine(
    DATABASE_URL,
    pool_size=10,        # একসাথে কতগুলো কানেকশন খোলা রাখা যাবে
    max_overflow=20,     # প্রয়োজনে অতিরিক্ত কতগুলো কানেকশন তৈরি হতে পারে
    pool_pre_ping=True   # কানেকশন ড্রপ হলে তা অটো চেক করবে
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ডিপেন্ডেন্সি ইনজেকশন ফাংশন
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()