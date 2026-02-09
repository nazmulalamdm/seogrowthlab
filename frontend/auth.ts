import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import { PrismaClient } from "@prisma/client"
import bcrypt from "bcryptjs"

// গ্লোবাল প্রিজমা ইনস্ট্যান্স (Next.js এর জন্য বেস্ট প্র্যাকটিস)
const globalForPrisma = global as unknown as { prisma: PrismaClient }
export const prisma = globalForPrisma.prisma || new PrismaClient()
if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma

export const { handlers, signIn, signOut, auth } = NextAuth({
  session: { strategy: "jwt" },
  providers: [
    Credentials({
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      authorize: async (credentials) => {
        if (!credentials?.email || !credentials?.password) {
          return null
        }

        // ✅ আপনার স্কিমা অনুযায়ী 'users' ব্যবহার করা হয়েছে
        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
        })

        if (!user || !user.password) {
          throw new Error("User not found.")
        }

        const isMatch = await bcrypt.compare(
          credentials.password as string,
          user.password
        )

        if (!isMatch) {
          throw new Error("Invalid password.")
        }

        return {
          id: user.id.toString(),
          name: user.name,
          email: user.email,
        }
      },
    }),
  ],
  pages: {
    signIn: '/login', 
  },
  callbacks: {
    // সেশনে ইউজার আইডি পাস করার জন্য
    async session({ session, token }) {
      if (token.sub && session.user) {
        session.user.id = token.sub
      }
      return session
    },
  },
})