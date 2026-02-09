from mcp.server.fastmcp import FastMCP  # pyright: ignore[reportMissingImports]
from sqlalchemy import text
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

# ১. এনভায়রনমেন্ট লোড করা (রুট ডিরেক্টরি থেকে)
# mcp_server.py যেহেতু backend ফোল্ডারে, তাই parent.parent ব্যবহার করে .env খুঁজে বের করা
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# ২. পাথ সেটআপ যাতে database.py খুঁজে পায়
# বর্তমান ফোল্ডার (backend) কে পাথে যোগ করা
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from database import engine  # সরাসরি ইমপোর্ট যেহেতু একই ফোল্ডারে আছে

# MCP সার্ভার তৈরি
mcp = FastMCP("SEO-Growth-Lab-Core")

@mcp.tool()
def check_system_health() -> str:
    """ডেটাবেজ কানেকশন এবং সিস্টেমের অবস্থা চেক করে।"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return "✅ System Health: Excellent. Database connected successfully!"
    except Exception as e:
        return f"❌ System Health: Critical. Error: {str(e)}"

@mcp.tool()
def run_custom_query(query: str) -> str:
    """সরাসরি এসকিউএল কোয়েরি রান করে ডাটাবেজ থেকে তথ্য আনে।"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchmany(5)
            if not rows:
                return "কোনো ডাটা পাওয়া যায়নি।"
            return str([dict(row._mapping) for row in rows])
    except Exception as e:
        return f"Error executing query: {str(e)}"

if __name__ == "__main__":
    mcp.run()