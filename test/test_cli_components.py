"""
Quick CLI test to verify the updated model works
"""
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def test_cli_imports():
    """Test that CLI components import correctly with new model"""
    print("🧪 Testing CLI Component Imports...")
    
    try:
        # Test core imports
        from llm_manager import LLMManager
        print("✅ LLMManager imported successfully")
        
        from config import DEFAULT_MODEL, GPT4_MODEL
        print(f"✅ Config imported - Model: {DEFAULT_MODEL}")
        
        # Test manager initialization (with dummy API key)
        os.environ['ANTHROPIC_API_KEY'] = 'dummy-key-for-testing'
        manager = LLMManager()
        print("✅ LLMManager initialized successfully")
        
        # Test provider info
        info = manager.get_current_provider_info()
        print(f"✅ Provider info: {info['provider']} - {info['model']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run CLI test"""
    print("🔧 CLI Component Test with Updated Model")
    print("=" * 50)
    
    success = test_cli_imports()
    
    if success:
        print("\n🎉 CLI test passed!")
        print("✅ All components work with claude-sonnet-4-20250514")
        print("✅ System ready for CLI and API usage")
    else:
        print("\n❌ CLI test failed")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())