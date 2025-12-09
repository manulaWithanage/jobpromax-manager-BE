from dotenv import load_dotenv
import os

load_dotenv()

REQUIRED_KEYS = [
    "CLERK_SECRET_KEY",
    "CLERK_ISSUER",
    "SUPER_ADMIN_EMAIL",
    "MONGODB_URI",
    "DATABASE_NAME"
]

print("--- Environment Variable Check ---")
all_present = True
for key in REQUIRED_KEYS:
    val = os.getenv(key)
    if val:
        # Print first few chars to verify it's not empty, but masked
        masked = val[:4] + "..." if len(val) > 4 else "***"
        print(f"✅ {key}: Found ({masked})")
    else:
        print(f"❌ {key}: MISSING")
        all_present = False

if all_present:
    print("\nSUCCESS: All required variables are set.")
else:
    print("\nFAILURE: Some variables are missing.")
