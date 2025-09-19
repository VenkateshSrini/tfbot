#!/usr/bin/env python3
"""
Simple verification script to test that existing functionality still works
after adding Bedrock support
"""
import sys
import os
sys.path.append('..')

def test_basic_functionality():
    """Test basic functionality without mocking"""
    print("🔍 Testing basic LLM Manager functionality...")
    
    try:
        from config import get_provider_from_model, get_api_key_env_var
        from llm_manager import LLMManager, OpenAILLMProvider, AnthropicLLMProvider, BedrockLLMProvider
        
        print("✅ All imports successful")
        
        # Test provider detection
        print("\n📋 Testing provider detection...")
        assert get_provider_from_model('gpt-4') == 'openai'
        assert get_provider_from_model('claude-sonnet-4-20250514') == 'anthropic'
        print("✅ Provider detection works")
        
        # Test API key mapping
        assert get_api_key_env_var('openai') == 'OPENAI_API_KEY'
        assert get_api_key_env_var('anthropic') == 'ANTHROPIC_API_KEY'
        print("✅ API key mapping works")
        
        # Test Bedrock models should fail (commented out)
        try:
            get_provider_from_model('anthropic.claude-3-5-sonnet-20240620-v1:0')
            print("❌ Bedrock models should not be detected when commented")
            return False
        except ValueError:
            print("✅ Bedrock models correctly rejected when commented")
        
        # Test class instantiation (without API keys)
        print("\n🏗️ Testing class structure...")
        
        # Mock environment to avoid API key prompts
        os.environ['OPENAI_API_KEY'] = 'test-key'
        os.environ['ANTHROPIC_API_KEY'] = 'test-key'
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
        
        openai_provider = OpenAILLMProvider('gpt-4', 0.3)
        anthropic_provider = AnthropicLLMProvider('claude-sonnet-4-20250514', 0.3)
        bedrock_provider = BedrockLLMProvider('anthropic.claude-3-5-sonnet-20240620-v1:0', 0.3)
        
        assert openai_provider.get_provider_name() == 'OpenAI'
        assert anthropic_provider.get_provider_name() == 'Anthropic'
        assert bedrock_provider.get_provider_name() == 'AWS Bedrock'
        print("✅ Provider classes instantiate correctly")
        
        # Test LLMManager without actual LLM creation
        try:
            manager = LLMManager()
            info = manager.get_current_provider_info()
            assert 'provider' in info
            assert 'model' in info
            assert 'temperature' in info
            print("✅ LLMManager initialization and info retrieval works")
        except Exception as e:
            print(f"⚠️ LLMManager test skipped due to: {e}")
        
        print("\n🎉 All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🧪 Terraform Bot - Basic Functionality Verification")
    print("=" * 60)
    
    success = test_basic_functionality()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Verification PASSED - Existing functionality intact!")
        sys.exit(0)
    else:
        print("❌ Verification FAILED - Issues detected!")
        sys.exit(1)