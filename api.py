import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to read the MapMyIndia key
api_key = os.environ.get("MAPMYINDIA_API_KEY")

if api_key:
    print("✓ API Key found!")
    print(f"  First 10 characters: {api_key[:10]}...")  # Show only first 10 for security
else:
    print("✗ API Key NOT found. Check your .env file.")