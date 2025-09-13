"""
Provider Switching Demo Script
Shows how to switch between OpenAI and Anthropic providers
"""

def show_current_config():
    """Show current configuration"""
    with open('../config.py', 'r') as f:
        lines = f.readlines()
    
    print("📋 Current Configuration in config.py:")
    print("-" * 50)
    
    for line in lines[7:17]:  # Show the model configuration section
        if line.strip():
            print(f"   {line.rstrip()}")
    
    print()

def show_switching_guide():
    """Show how to switch providers"""
    print("🔄 How to Switch Providers:")
    print("-" * 50)
    print()
    
    print("📱 TO SWITCH TO OPENAI:")
    print("1. Edit config.py:")
    print("   # Comment out Anthropic models:")
    print("   # DEFAULT_MODEL = 'claude-3-5-sonnet-20240620'")
    print("   # GPT4_MODEL = 'claude-3-5-sonnet-20240620'")
    print()
    print("   # Uncomment OpenAI models:")
    print("   DEFAULT_MODEL = 'gpt-4.1'")
    print("   GPT4_MODEL = 'gpt-4.1'")
    print()
    print("2. Set environment variable:")
    print("   export OPENAI_API_KEY='your-openai-key'")
    print()
    print("3. Restart the application")
    print()
    
    print("🧠 TO SWITCH TO ANTHROPIC:")
    print("1. Edit config.py:")
    print("   # Comment out OpenAI models:")
    print("   # DEFAULT_MODEL = 'gpt-4.1'")
    print("   # GPT4_MODEL = 'gpt-4.1'")
    print()
    print("   # Uncomment Anthropic models:")
    print("   DEFAULT_MODEL = 'claude-3-5-sonnet-20240620'")
    print("   GPT4_MODEL = 'claude-3-5-sonnet-20240620'")
    print()
    print("2. Set environment variable:")
    print("   export ANTHROPIC_API_KEY='your-anthropic-key'")
    print()
    print("3. Restart the application")
    print()

def show_supported_models():
    """Show supported models for each provider"""
    print("🤖 Supported Models:")
    print("-" * 50)
    print()
    print("OpenAI Models:")
    print("  • gpt-4.1")
    print("  • gpt-4")
    print("  • gpt-4-turbo")
    print("  • gpt-3.5-turbo")
    print()
    print("Anthropic Models:")
    print("  • claude-3-5-sonnet-20240620 (recommended)")
    print("  • claude-3-sonnet-20240229")
    print("  • claude-3-haiku-20240307")
    print("  • claude-3-opus-20240229")
    print()

def main():
    """Main demo function"""
    print("🚀 Terraform Bot - Multi-Provider LLM Demo")
    print("=" * 60)
    print()
    
    show_current_config()
    show_supported_models()
    show_switching_guide()
    
    print("✅ Key Benefits:")
    print("  • Automatic provider detection based on model name")
    print("  • No code changes required to switch providers")
    print("  • Backward compatibility with existing code")
    print("  • Robust error handling and clear error messages")
    print("  • Instance caching for better performance")
    print()
    
    print("🧪 To verify the system is working:")
    print("  python test/verify_multi_provider.py")
    print()
    
    print("📚 For detailed documentation:")
    print("  See documentation/MULTI_PROVIDER_LLM_GUIDE.md")

if __name__ == '__main__':
    main()