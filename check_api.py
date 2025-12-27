import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("MAPMYINDIA_API_KEY")

print("API Key Check:")
print(f"  Length: {len(api_key) if api_key else 0} characters")
print(f"  First 10 chars: {api_key[:10] if api_key else 'NOT FOUND'}")
print(f"  Last 5 chars: {api_key[-5:] if api_key else 'NOT FOUND'}")
print(f"\nFull key: {api_key}")