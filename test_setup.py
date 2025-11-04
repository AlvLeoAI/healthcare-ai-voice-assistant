#!/usr/bin/env python3
"""
Quick test script to verify installation
"""

import sys

print("Testing Healthcare Voice Assistant Setup...\n")

# Test 1: Python version
print("1. Python Version:")
print(f"   {sys.version}")
assert sys.version_info >= (3, 9), "Python 3.9+ required"
print("   ✓ Python version OK\n")

# Test 2: Import dependencies
print("2. Testing Dependencies:")
try:
    import openai
    print("   ✓ openai installed")
except ImportError:
    print("   ✗ openai not installed - run: pip install -r requirements.txt")

try:
    import elevenlabs
    print("   ✓ elevenlabs installed")
except ImportError:
    print("   ✗ elevenlabs not installed - run: pip install -r requirements.txt")

try:
    from dotenv import load_dotenv
    print("   ✓ python-dotenv installed")
except ImportError:
    print("   ✗ python-dotenv not installed - run: pip install -r requirements.txt")

print()

# Test 3: Check data files
print("3. Checking Data Files:")
from pathlib import Path

data_files = [
    "data/clinic_info.json",
    "data/appointments.json",
    "data/insurance_providers.json"
]

for file in data_files:
    if Path(file).exists():
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} missing")

print()

# Test 4: Check .env
print("4. Environment Configuration:")
load_dotenv()
import os

if os.getenv("OPENAI_API_KEY"):
    print("   ✓ OPENAI_API_KEY is set")
else:
    print("   ✗ OPENAI_API_KEY not set - copy .env.example to .env and add your key")

if os.getenv("ELEVENLABS_API_KEY"):
    print("   ✓ ELEVENLABS_API_KEY is set")
else:
    print("   ✗ ELEVENLABS_API_KEY not set - copy .env.example to .env and add your key")

print("\n" + "="*60)
print("Setup test complete!")
print("="*60)
print("\nTo run the assistant:")
print("  python main.py")
