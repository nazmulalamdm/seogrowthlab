/** @type {import('next').NextConfig} */
const nextConfig = {
  // প্রিজমা এবং বিকিপ্টকে সার্ভার সাইড প্যাকেজ হিসেবে ট্রিট করবে
  serverExternalPackages: ['@prisma/client', 'bcryptjs'],
  
  // টেলউইন্ড বা অন্যান্য কনফিগ এখানে সাধারণত লাগে না, 
  // তবে আপনি চাইলে অন্য অপশন যোগ করতে পারেন।
};

export default nextConfig;