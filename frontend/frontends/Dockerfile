FROM node:22-alpine

WORKDIR /app

# ১. প্যাকেজ ফাইল কপি (সামনে frontend/ যোগ করা হয়েছে)
# কারণ আমরা রুট ফোল্ডার থেকে ফাইলগুলো খুঁজছি
COPY frontend/package*.json ./

# ২. ডিপেন্ডেন্সি ইন্সটল
RUN npm install



# ... (আগের কোড) ...
COPY frontend/prisma ./prisma/

# কনফিগ ফাইল কপি করা বাধ্যতামূলক
COPY frontend/prisma.config.ts ./

# ডামি এনভায়রনমেন্ট
ENV DATABASE_URL_PRISMA="postgresql://dummy:5432/dummy_db"

RUN npx prisma generate
# ... (বাকি কোড) ...

# ৪. প্রিজমা ক্লায়েন্ট জেনারেট
RUN npx prisma generate

# ৫. সোর্স কোড কপি (সামনে frontend/ যোগ করা হয়েছে)
COPY frontend/ .

# ৬. বিল্ড করা
RUN npm run build

EXPOSE 3000

# রান কমান্ড কম্পোজ ফাইল থেকে আসবে