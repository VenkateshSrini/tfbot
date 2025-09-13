"""
Simple verification script for multi-provider LLM functionality
"""
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from llm_manager import LLMManager
from config import get_provider_from_model

def test_provider_detection():
    """Test provider detection functionality"""
    print("🔍 Testing Provider Detection...")
    
    # Test OpenAI detection
    openai_models = ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo']
    for model in openai_models:
        provider = get_provider_from_model(model)
        assert provider == 'openai', f"Expected 'openai' for {model}, got {provider}"
        print(f"✅ {model} -> {provider}")
    
    # Test Anthropic detection
    anthropic_models = ['claude-sonnet-4-20250514', 'claude-3-5-sonnet-20240620', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307']
    for model in anthropic_models:
        provider = get_provider_from_model(model)
        assert provider == 'anthropic', f"Expected 'anthropic' for {model}, got {provider}"
        print(f"✅ {model} -> {provider}")
    
    print("✅ Provider detection working correctly!\n")

def test_llm_manager():
    """Test LLM Manager initialization and basic functionality"""
    print("🤖 Testing LLM Manager...")
    
    # Set a dummy API key to avoid prompting
    os.environ['ANTHROPIC_API_KEY'] = 'dummy-key-for-testing'
    
    try:
        manager = LLMManager()
        print("✅ LLM Manager initialized successfully")
        
        # Test provider info
        info = manager.get_current_provider_info()
        print(f"✅ Current provider: {info['provider']}")
        print(f"✅ Current model: {info['model']}")
        print(f"✅ Temperature: {info['temperature']}")
        
        # Verify the model is correct
        expected_model = "claude-sonnet-4-20250514"
        if info['model'] == expected_model:
            print(f"✅ Model correctly configured: {expected_model}")
        else:
            print(f"❌ Model mismatch. Expected: {expected_model}, Got: {info['model']}")
            return False
        
        # Test backward compatibility methods
        manager.get_default_llm  # Should not raise error
        manager.get_gpt4_llm     # Should not raise error
        manager.get_gpt35_llm    # Should not raise error
        print("✅ Backward compatibility methods available")
        
    except Exception as e:
        print(f"❌ Error testing LLM Manager: {e}")
        return False
    
    print("✅ LLM Manager working correctly!\n")
    return True

def main():
    """Run all verification tests"""
    print("🧪 Terraform Bot Multi-Provider LLM Verification")
    print("=" * 60)
    
    try:
        test_provider_detection()
        success = test_llm_manager()
        
        if success:
            print("🎉 All verifications passed!")
            print("✅ Multi-provider LLM system is working correctly")
            print("\n📋 To switch providers:")
            print("1. Edit config.py to change DEFAULT_MODEL")
            print("2. Set appropriate API key environment variable")
            print("3. Restart the application")
        else:
            print("❌ Some verifications failed")
            return 1
            
    except Exception as e:
        print(f"❌ Verification failed with error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())