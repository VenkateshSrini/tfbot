"""
Simple configuration validation test
"""
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from config import DEFAULT_MODEL, GPT4_MODEL, get_provider_from_model

def test_model_config():
    """Test the current model configuration"""
    print("🔧 Testing Model Configuration...")
    print(f"   DEFAULT_MODEL: {DEFAULT_MODEL}")
    print(f"   GPT4_MODEL: {GPT4_MODEL}")
    
    # Test provider detection
    provider = get_provider_from_model(DEFAULT_MODEL)
    print(f"   Provider detected: {provider}")
    
    # Validate configuration
    if DEFAULT_MODEL == GPT4_MODEL:
        print("✅ DEFAULT_MODEL and GPT4_MODEL are consistent")
    else:
        print("❌ DEFAULT_MODEL and GPT4_MODEL are different")
        return False
    
    if provider == 'anthropic':
        print("✅ Provider correctly detected as Anthropic")
    elif provider == 'openai':
        print("✅ Provider correctly detected as OpenAI")
    else:
        print(f"❌ Unknown provider: {provider}")
        return False
    
    # Test specific model
    if DEFAULT_MODEL == 'claude-sonnet-4-20250514':
        print("✅ Model correctly set to claude-sonnet-4-20250514")
    else:
        print(f"ℹ️  Model set to: {DEFAULT_MODEL}")
    
    return True

def main():
    """Run configuration test"""
    print("🧪 Configuration Validation Test")
    print("=" * 50)
    
    success = test_model_config()
    
    if success:
        print("\n🎉 Configuration test passed!")
        print("✅ Model details are correct")
    else:
        print("\n❌ Configuration test failed")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())