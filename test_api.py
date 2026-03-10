#!/usr/bin/env python3
"""
Quick connectivity check for the OpenAI API configuration.

This script is meant for local environment validation before a large analysis
run. It confirms that ``OPENAI_API_KEY`` is present and that a simple chat
completion can be created successfully.
"""

import os
from dotenv import load_dotenv
import openai


def main() -> None:
    """Load the local API key and perform a minimal completion request."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in .env file")
        raise SystemExit(1)

    print("✅ API key loaded from .env file")
    print(f"   Key starts with: {api_key[:15]}...")
    print(f"   Key length: {len(api_key)} characters")

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API connection successful' in 5 words or less"}],
            max_tokens=10
        )
        print(f"\n✅ API Test Response: {response.choices[0].message.content}")
        print("\n🎉 Everything is configured correctly! You're ready to analyze privacy policies.")

    except openai.AuthenticationError:
        print("\n❌ Authentication failed. Please check your API key.")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
