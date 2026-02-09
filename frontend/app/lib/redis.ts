import { createClient } from 'redis';

const redisClient = createClient({
    // আপনার .env ফাইল থেকে REDIS_URL নিচ্ছে, না থাকলে ডিফল্ট লোকালহোস্ট ব্যবহার করবে
    url: process.env.REDIS_URL || 'redis://localhost:6379'
});

redisClient.on('error', (err) => console.log('Redis Client Error', err));

if (!redisClient.isOpen) {
    redisClient.connect();
}

export default redisClient;