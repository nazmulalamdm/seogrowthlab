import { StateGraph, END } from "@langchain/langgraph";

// ১. স্টেট ডিফাইন করা (এটি ডেটা হোল্ডার হিসেবে কাজ করবে)
const AuditState = {
  url: "",
  raw_data: "",
  audit_report: "",
};

// ২. নোড তৈরি করা (n8n-এর একেকটি নোডের মতো)
const crawlNode = async (state: typeof AuditState) => {
  console.log("Crawling URL:", state.url);
  // ভবিষ্যতে এখানে আপনার Rust ক্রলার কাজ করবে
  return { ...state, raw_data: "Example Page Title and Meta Data" };
};

const analyzeNode = async (state: typeof AuditState) => {
  console.log("Analyzing Data...");
  // এখানে AI ডেটা এনালাইসিস করবে
  return { ...state, audit_report: "SEO Score: 85/100. Meta Title is good." };
};

const saveNode = async (state: typeof AuditState) => {
  console.log("Saving to Database and Redis...");
  // এখানে আপনার Prisma এবং Redis-এ ডেটা সেভ হবে
  return state;
};

// ৩. গ্রাফ বা ওয়ার্কফ্লো তৈরি করা
// ৩. গ্রাফ বা ওয়ার্কফ্লো তৈরি করা
const workflow = new StateGraph({
  // channels-এ সরাসরি AuditState না দিয়ে একটি অবজেক্ট দিন
  channels: {
    url: { reducer: (oldVal: string, newVal: string) => newVal || oldVal },
    raw_data: { reducer: (oldVal: string, newVal: string) => newVal || oldVal },
    audit_report: { reducer: (oldVal: string, newVal: string) => newVal || oldVal }
  } as any,
})
  .addNode("crawler", crawlNode)
  .addNode("analyzer", analyzeNode)
  .addNode("saver", saveNode)
  .addEdge("__start__", "crawler")
  .addEdge("crawler", "analyzer")
  .addEdge("analyzer", "saver")
  .addEdge("saver", END);

export const seoAuditApp = workflow.compile();