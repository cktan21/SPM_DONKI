#!/usr/bin/env python3
"""
Internal API Key Generator
Run this script to generate secure API keys for service-to-service communication
"""

import secrets
import string
import uuid
import hashlib
from datetime import datetime

def generate_secure_api_key(length=64):
    """Generate a cryptographically secure API key"""
    alphabet = string.ascii_letters + string.digits + "-_"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_uuid_based_key():
    """Generate API key based on UUID4 (alternative method)"""
    return f"internal_{uuid.uuid4().hex}_{uuid.uuid4().hex}"

def generate_prefixed_key(service_name="microservice"):
    """Generate API key with service prefix"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_part = secrets.token_urlsafe(32)
    return f"{service_name}_internal_{timestamp}_{random_part}"

def generate_hash_based_key():
    """Generate hash-based API key"""
    # Combine multiple random sources
    data = f"{secrets.token_hex(16)}_{datetime.now().isoformat()}_{secrets.randbits(128)}"
    return hashlib.sha256(data.encode()).hexdigest()

if __name__ == "__main__":
    print("🔐 Internal API Key Generator")
    print("=" * 50)
    
    print("\n1. Standard secure key (64 chars):")
    print(generate_secure_api_key())
    
    print("\n2. UUID-based key:")
    print(generate_uuid_based_key())
    
    print("\n3. Prefixed key with timestamp:")
    print(generate_prefixed_key("taskservice"))
    
    print("\n4. Hash-based key (SHA256):")
    print(generate_hash_based_key())
    
    print("\n5. Extra long key (128 chars):")
    print(generate_secure_api_key(128))
    
    print("\n💡 Recommendation: Use option 1 or 5 for maximum security")
    print("⚠️  Store this key securely in your .env files!")