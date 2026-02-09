FROM node:22-alpine

WORKDIR /app

# ১. প্যাকেজ ফাইল কপি
COPY frontend/package*.json ./

# ২. ডিপেন্ডেন্সি ইন্সটল (এখানেই Prisma 7 ইন্সটল হচ্ছে)
RUN npm install

# ৩. প্রিজমা ফোল্ডার কপি
COPY frontend/prisma ./prisma/

# ৪. [গুরুত্বপূর্ণ FIX] প্রিজমা ৭ কনফিগারেশন ফাইল কপি
# এই ফাইলটি কপি না করলে Prisma 7 জেনারেট কাজ করবে না
COPY frontend/prisma.config.ts ./

# ৫. ডামি এনভায়রনমেন্ট সেট করা
# আপনার কনফিগ ফাইলে 'DATABASE_URL_PRISMA' আছে, তাই বিল্ডের সময় এটি পেতেই হবে
ENV DATABASE_URL_PRISMA="postgresql://dummy:5432/dummy_db"

# ৬. প্রিজমা ক্লায়েন্ট জেনারেট
# এখন এটি কনফিগ ফাইল এবং ENV দুটোই পাবে
RUN npx prisma generate

# ৭. বাকি সোর্স কোড কপি
COPY frontend/ .

# ৮. নেক্সট জেএস বিল্ড
# টেলিমেট্রি বন্ধ রাখা ভালো (অপশনাল)
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]