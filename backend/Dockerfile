FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gcc libpq-dev build-essential curl nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ১. স্কিমা কপি করুন (যেটাতে url নেই)
COPY frontend/prisma/schema.prisma ./prisma/schema.prisma

# ২. [FIX] Python এর জন্য স্কিমায় URL লাইনটি ইনজেক্ট করা
# কারণ Python Client কনফিগ ফাইল বোঝে না, তার স্কিমায় URL লাগে
RUN sed -i 's/provider = "postgresql"/provider = "postgresql"\n  url = env("DATABASE_URL_PRISMA")/' ./prisma/schema.prisma

# ৩. ডামি এনভায়রনমেন্ট (বিল্ড পাস করার জন্য)
ENV DATABASE_URL_PRISMA="postgresql://dummy:5432/dummy_db"

# ৪. এখন জেনারেট করুন (এটি এখন কাজ করবে)
RUN prisma generate

COPY backend/ .

EXPOSE 8000
CMD ["python", "main.py"]