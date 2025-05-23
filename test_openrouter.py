#!/usr/bin/env python3
"""
Test script to verify OpenRouter API integration
"""

import sys
import os
sys.path.append('backend')

from backend.utils import openrouter_api_key, openai_api_key
from backend.persona.prompt_template.gpt_structure import ChatGPT_request

def test_openrouter():
    print("Testing OpenRouter API...")
    print(f"OpenRouter API Key: {openrouter_api_key[:20]}..." if openrouter_api_key else "No OpenRouter key found")
    print(f"OpenAI API Key: {openai_api_key[:20]}..." if openai_api_key else "No OpenAI key found")
    
    # Test a simple prompt
    test_prompt = "Hello! Please respond with exactly: 'OpenRouter is working correctly.'"
    
    try:
        response = ChatGPT_request(test_prompt)
        print(f"✅ OpenRouter Response: {response}")
        return True
    except Exception as e:
        print(f"❌ OpenRouter Error: {e}")
        return False

if __name__ == "__main__":
    test_openrouter()
